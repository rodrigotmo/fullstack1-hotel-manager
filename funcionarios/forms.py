# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Funcionario  # ou use get_user_model() se for customizado

class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'})
    )
    administrador = forms.BooleanField(
        label='Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Funcionario
        fields = ['nome', 'username', 'senha', 'administrador']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome de usuário', 'required': True}),
        }
