from datetime import date
from django import forms
from clientes.models import Cliente

class ReservaInicialForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(ativo=True), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    data_reserva_previsao_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()}),
        required=True
    )
    data_reserva_previsao_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('data_reserva_previsao_inicio')
        fim = cleaned_data.get('data_reserva_previsao_fim')

        if inicio and fim and inicio >= fim:
            raise forms.ValidationError("A data de início deve ser anterior à data de fim.")

        return cleaned_data
