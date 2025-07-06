from datetime import date
from django import forms
from .models import TarifaTipoQuarto, TipoQuarto, Quarto, Ocorrencia, StatusQuarto

class TipoQuartoForm(forms.ModelForm):
    class Meta:
        model = TipoQuarto
        fields = ['nome_tipo_quarto']
        labels = {
            'nome_tipo_quarto': 'Nome',
        }
        widgets = {
            'nome_tipo_quarto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do tipo de quarto'
            }),
        }


class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'capacidade', 'tipo_quarto', 'foto']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_quarto': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['quarto', 'descricao']
        widgets = {
            'quarto': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            status_removido = StatusQuarto.REMOVIDO()
            self.fields['quarto'].queryset = Quarto.objects.exclude(status_quarto=status_removido)
        except StatusQuarto.DoesNotExist:
            self.fields['quarto'].queryset = Quarto.objects.all()

    def clean_quarto(self):
        quarto = self.cleaned_data.get('quarto')
        if not Quarto.objects.filter(id=quarto.id).exists():
            raise forms.ValidationError("Quarto inválido.")
        return quarto
    
    
class TarifaTipoQuartoForm(forms.ModelForm):
    class Meta:
        model = TarifaTipoQuarto
        fields = [
            'tipo_quarto',
            'nome_tarifa_tipo_quarto',
            'data_inicio_vigencia',
            'data_fim_vigencia',
            'valor_diaria',
        ]
        widgets = {
            'data_inicio_vigencia': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'data_fim_vigencia': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'min': date.today().isoformat()},
                format='%Y-%m-%d'
            ),
            'tipo_quarto': forms.Select(attrs={'class': 'form-control'}),
            'nome_tarifa_tipo_quarto': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_diaria': forms.NumberInput(attrs={'class': 'form-control'}),
        }
