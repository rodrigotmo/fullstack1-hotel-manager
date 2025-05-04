from django.shortcuts import render
from funcionarios.models import Funcionario
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import FuncionarioForm


def funcionarios(request):
    if request.user.is_authenticated and request.user.is_staff:
        funcionarios = Funcionario.objects.all()
        return render(request, 'funcionario/funcionarios.html', {'funcionarios': funcionarios})
    else:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

def cadastrar_funcionario(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            if Funcionario.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, 'Usuário já cadastrado.')
                return redirect('funcionarios')

            funcionario = Funcionario(
                username=form.cleaned_data['username'],
                nome=form.cleaned_data['nome'],
                is_staff=form.cleaned_data['administrador']
            )
            funcionario.set_password(form.cleaned_data['senha'])
            funcionario.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('funcionarios')
    else:
        form = FuncionarioForm()

    return render(request, 'funcionario/cadastro.html', {'form': form})


def editar_funcionario(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            username = form.cleaned_data['username']
            if Funcionario.objects.exclude(id=id).filter(username=username).exists():
                messages.error(request, 'Usuário já cadastrado.')
                return redirect('editar_funcionario', id=id)

            funcionario.nome = form.cleaned_data['nome']
            funcionario.username = username
            funcionario.is_staff = form.cleaned_data['administrador']
            if form.cleaned_data['senha']:
                funcionario.set_password(form.cleaned_data['senha'])
            funcionario.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario, initial={'administrador': funcionario.is_staff})

    return render(request, 'funcionario/cadastro.html', {'form': form, 'funcionario': funcionario})

def desativar_funcionario(request, id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.ativo = False
    funcionario.save()
    messages.success(request, "Funcionário desativado com sucesso!")
    return redirect('funcionarios')

def ativar_funcionario(request, id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.ativo = True
    funcionario.save()
    messages.success(request, "Funcionário ativado com sucesso!")
    return redirect('funcionarios')

