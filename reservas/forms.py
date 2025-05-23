from datetime import date, timezone
from django import forms
from django.db.models import Q
from quartos.models import StatusQuarto, TarifaTipoQuarto
from .models import Reserva, Cliente, Quarto, StatusReserva

class ReservaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(ativo=True), required=True)
    quarto = forms.ModelChoiceField(queryset=Quarto.objects.none(), required=True)

    class Meta:
        model = Reserva
        fields = ['cliente', 'data_reserva_previsao_inicio', 'data_reserva_previsao_fim', 'quarto']
        widgets = {
            'data_reserva_previsao_inicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()},
                format='%Y-%m-%d'
            ),
            'data_reserva_previsao_fim': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()},
                format='%Y-%m-%d'
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user 
        self.fields['quarto'].queryset = Quarto.objects.exclude(
            Q(status_quarto_id=StatusQuarto.REMOVIDO()) |
            Q(reserva_liberada=False)
        )

        if 'data_reserva_previsao_inicio' in self.data and 'data_reserva_previsao_fim' in self.data:
            self.atualizar_quartos_disponiveis()

    def atualizar_quartos_disponiveis(self):
        data_inicio = self.data.get('data_reserva_previsao_inicio')
        data_fim = self.data.get('data_reserva_previsao_fim')

        if data_inicio and data_fim:
            quartos_ocupados = Reserva.objects.filter(
                data_reserva_previsao_fim__gte=data_inicio,
                data_reserva_previsao_inicio__lte=data_fim
            ).values_list('quarto_id', flat=True)

            self.fields['quarto'].queryset = Quarto.objects.exclude(
                Q(id__in=quartos_ocupados) |
                Q(status_quarto_id=StatusQuarto.REMOVIDO()) |
                Q(reserva_liberada=False)
            )

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
        reserva.data_reserva_criada = date.today()
        reserva.status_reserva = StatusReserva.RESERVADA()
        tarifa = TarifaTipoQuarto.objects.filter(
            tipo_quarto=reserva.quarto.tipo_quarto,
            data_inicio_vigencia__lte=reserva.data_reserva_previsao_inicio,
            data_fim_vigencia__gte=reserva.data_reserva_previsao_fim
        ).first()

        if not tarifa:
            raise forms.ValidationError("Não há tarifa definida para esse tipo de quarto na data selecionada.")
    
        reserva.tarifa_tipo_quarto = tarifa
        
        if commit:
            reserva.save()
        return reserva