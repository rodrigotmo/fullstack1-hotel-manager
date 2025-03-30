from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from hotelapp.models import Funcionario
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'home.html')
        else:    
            return render(request, 'login.html')
        
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        funcionario = authenticate(request, username=usuario, password=senha)
        if funcionario is not None:
            auth_login(request, funcionario)
            messages.success(request, 'Bem-vindo(a), {}'.format(request.user.username))
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')
        
        
        
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('login')
    else:
        return redirect('login')
    
    
        
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        messages.error(request, 'Você precisa estar logado para acessar esta página.')  
        return redirect('login')
    
    

def funcionarios(request):
    if request.user.is_authenticated and request.user.is_staff:
        funcionarios = Funcionario.objects.all()
        return render(request, 'funcionarios/funcionarios.html', {'funcionarios': funcionarios})
    else:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')


def cadastrar_funcionario(request):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'funcionarios/cadastro.html')
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
        return render(request, 'funcionarios/cadastro.html', {'funcionario': funcionario})
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        administrador = 'administrador' in request.POST 

        if nome and usuario:
            funcionario.nome = nome
            funcionario.usuario = usuario
            if senha:  
                funcionario.set_password(senha)
            funcionario.is_staff = administrador
            funcionario.save()

            messages.success(request, "Funcionário atualizado com sucesso!")
            return redirect('funcionarios')
        else:
            messages.error(request, "Nome e Usuário são obrigatórios!")

