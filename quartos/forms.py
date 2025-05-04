from django import forms
from .models import TipoQuarto, Quarto, Ocorrencia

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
                'placeholder': 'Digite o nome do tipo de quarto',
                'required': True
            }),
        }


class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'capacidade', 'tipo_quarto']
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

    def clean_quarto(self):
        quarto = self.cleaned_data.get('quarto')
        if not Quarto.objects.filter(id=quarto.id).exists():
            raise forms.ValidationError("Quarto inválido.")
        return quarto