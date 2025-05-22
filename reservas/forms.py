from datetime import date, timezone
from django import forms
from .models import Reserva, Cliente, Quarto

class ReservaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(ativo=True), required=True)
    data_reserva_previsao_inicio = forms.DateField(widget=forms.SelectDateWidget, required=True)
    data_reserva_previsao_fim = forms.DateField(widget=forms.SelectDateWidget, required=True)
    quarto = forms.ModelChoiceField(queryset=Quarto.objects.none(), required=True)

    class Meta:
        model = Reserva
        fields = ['cliente', 'data_reserva_previsao_inicio', 'data_reserva_previsao_fim', 'quarto']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Usuário logado
        self.fields['quarto'].queryset = Quarto.objects.all()

        if 'data_reserva_previsao_inicio' in self.data and 'data_reserva_previsao_fim' in self.data:
            self.atualizar_quartos_disponiveis()

    def atualizar_quartos_disponiveis(self):
        data_inicio = self.cleaned_data.get('data_reserva_previsao_inicio')
        data_fim = self.cleaned_data.get('data_reserva_previsao_fim')

        if data_inicio and data_fim:
            quartos_ocupados = Reserva.objects.filter(
                data_reserva_previsao_fim__gte=data_inicio,
                data_reserva_previsao_inicio__lte=data_fim
            ).values_list('quarto_id', flat=True)

            self.fields['quarto'].queryset = Quarto.objects.exclude(id__in=quartos_ocupados)

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('data_reserva_previsao_inicio')
        fim = cleaned_data.get('data_reserva_previsao_fim')

        if inicio and fim and inicio > fim:
            raise forms.ValidationError("A data de início deve ser anterior à data de fim.")

        return cleaned_data

    def save(self, commit=True):
        reserva = super().save(commit=False)
        reserva.funcionario = self.user 
        reserva.data_reserva_criada = timezone.now().date()
        if commit:
            reserva.save()
        return reserva