from django.shortcuts import render
from funcionarios.models import Funcionario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

# Create your views here.

def funcionarios(request):
    if request.user.is_authenticated and request.user.is_staff:
        funcionarios = Funcionario.objects.all()
        return render(request, 'funcionarios.html', {'funcionarios': funcionarios})
    else:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

def cadastrar_funcionario(request):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        nome = request.POST.get('nome')
        administrador = request.POST.get('administrador')
        
        funcionario = Funcionario.objects.filter(username=username).first()
        if funcionario:
            messages.error(request, 'Usuário já cadastrado')
            return redirect('funcionarios')
        else:
            if administrador == 'on':
                is_staff = True
            else:
                is_staff = False
                
            funcionario = Funcionario.objects.create_user(
                username=username,
                password=password,
                nome=nome,
                is_staff=is_staff
            )
            funcionario.save()
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('funcionarios')

def editar_funcionario(request,id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    funcionario = get_object_or_404(Funcionario, id=id)
    if request.method == 'GET':
        return render(request, 'cadastro.html', {'funcionario': funcionario})
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        administrador = 'administrador' in request.POST 

        outro_funcionario = Funcionario.objects.exclude(id=id).filter(username=username).first()
        if outro_funcionario:
            messages.error(request, 'Usuário já cadastrado')
            return redirect('editar_funcionario', id=id)
            
        if nome and username:
            funcionario.nome = nome
            funcionario.username = username
            if password:  
                funcionario.set_password(password)
            funcionario.is_staff = administrador
            funcionario.save()

            messages.success(request, "Funcionário atualizado com sucesso!")
            return redirect('funcionarios')
        else:
            messages.error(request, "Nome e Usuário são obrigatórios!")
            return redirect('editar_funcionario', id=id)

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

