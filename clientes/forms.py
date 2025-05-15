# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente  # ou use get_user_model() se for customizado

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'documento', 'telefone', 'endereco']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome', 'required': True}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o documento', 'required': True}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone', 'required': True}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço', 'required': True}),
        }
