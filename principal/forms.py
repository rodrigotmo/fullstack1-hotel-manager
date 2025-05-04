# forms.py
from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite seu usuário',
        'id': 'usuario',
        'required': True
    }))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite sua senha',
        'id': 'senha',
        'required': True
    }))
