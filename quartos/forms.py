# forms.py
from django import forms
from .models import TipoQuarto, Quarto

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

