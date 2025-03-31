from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from hotelapp.models import Funcionario, Quarto, Reserva, Cliente, Ocorrencia, StatusQuarto, StatusReserva, TipoQuarto
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
        if funcionario is not None and funcionario.ativo:
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
        # Obter os objetos de StatusQuarto e StatusReserva para filtro
        status_liberado = StatusQuarto.objects.get(nome_status_quarto='Liberado')
        status_indisponivel = StatusQuarto.objects.get(nome_status_quarto='Indisponível')
        status_em_uso = StatusQuarto.objects.get(nome_status_quarto='Em uso')

        status_reservada = StatusReserva.objects.get(nome_status_reserva='Reservada')
        status_em_andamento = StatusReserva.objects.get(nome_status_reserva='Em andamento')
        status_finalizada = StatusReserva.objects.get(nome_status_reserva='Finalizada')
        status_cancelada = StatusReserva.objects.get(nome_status_reserva='Cancelada')

        dados_dashboard = {
            'qtd_funcionarios': Funcionario.objects.all().count(),
            'qtd_funcionarios_ativos': Funcionario.objects.filter(ativo=True).count(),
            'qtd_funcionarios_inativos': Funcionario.objects.filter(ativo=False).count(),
            
            'qtd_clientes': Cliente.objects.all().count(),
            'qtd_clientes_ativos': Cliente.objects.filter(ativo=True).count(),
            'qtd_clientes_inativos': Cliente.objects.filter(ativo=False).count(),
            
            'qtd_quartos': Quarto.objects.all().count(),
            'qtd_quartos_disponivel': Quarto.objects.filter(status_quarto=status_liberado).count(),
            'qtd_quartos_indisponivel': Quarto.objects.filter(status_quarto=status_indisponivel).count(),
            'qtd_quartos_em_uso': Quarto.objects.filter(status_quarto=status_em_uso).count(),
            
            'qtd_reservas': Reserva.objects.all().count(),
            'qtd_reservas_ativas': Reserva.objects.filter(status_reserva__in=[status_reservada, status_em_andamento]).count(),
            'qtd_reservas_finalizadas': Reserva.objects.filter(status_reserva=status_finalizada).count(),
            'qtd_reservas_canceladas': Reserva.objects.filter(status_reserva=status_cancelada).count(),
            
            'qtd_ocorrencias': Ocorrencia.objects.all().count(),
            'qtd_ocorrencias_ativas': Ocorrencia.objects.filter(finalizada=False).count(),
            'qtd_ocorrencias_finalizadas': Ocorrencia.objects.filter(finalizada=True).count(),
        }
        
        return render(request, 'home.html', dados_dashboard)
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



def quartos(request):
    if request.user.is_authenticated and request.user.is_staff:
        quartos = Quarto.objects.all()
        return render(request, 'quartos/quartos.html', {'quartos': quartos})
    else:
        messages.error(request, 'Você precisa estar logado como administrador para acessar esta página.')
        return redirect('home')
    
def cadastrar_quarto(request):
    if not request.user.is_authenticated and request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    if request.method == 'GET':
        tipos_quarto = TipoQuarto.objects.all()
        return render(request, 'quartos/cadastro.html', {'tipos_quarto': tipos_quarto, 'quarto': None})
    elif request.method == 'POST':
        numero = request.POST.get('numero')
        capacidade = request.POST.get('capacidade')
        tipo = request.POST.get('tipo_quarto')
        status = 1  # Status padrão para "Liberado"
        
        quarto = Quarto.objects.filter(numero=numero).first()
        if quarto:
            messages.error(request, 'Quarto já cadastrado')
            return redirect('quartos')
        elif numero and tipo and capacidade and status:
            tipo = TipoQuarto.objects.filter(id=tipo).first()
            if tipo:
                quarto = Quarto.objects.create(
                    numero=numero,
                    capacidade=capacidade,
                    tipo_quarto_id=tipo.id,
                    status_quarto_id=status,
                )
                quarto.save()
                messages.success(request, 'Quarto cadastrado com sucesso.')
                return redirect('quartos')
            else:
                messages.error(request, 'Tipo de quarto inválido')
                return redirect('quartos')
        else:
            messages.error(request, 'Número, Tipo e Capacidade são obrigatórios!')  
            return redirect('cadastrar_quarto')
        
def editar_quarto(request,id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    quarto = get_object_or_404(Quarto, id=id)
    if request.method == 'GET':
        tipos_quarto = TipoQuarto.objects.all()
        return render(request, 'quartos/cadastro.html', {'quarto': quarto, 'tipos_quarto': tipos_quarto})
    
    elif request.method == 'POST':
        numero = request.POST.get('numero')
        capacidade = request.POST.get('capacidade')
        tipo = request.POST.get('tipo_quarto')
        if numero and capacidade and tipo:
            tipo = TipoQuarto.objects.filter(id=tipo).first()
            if tipo:
                quarto.numero = numero
                quarto.capacidade = capacidade
                quarto.tipo_quarto_id = tipo
                quarto.save()
                messages.success(request, 'Quarto atualizado com sucesso.')
                return redirect('quartos')
            else:
                messages.error(request, 'Tipo de quarto inválido')
                return redirect('quartos')
        else:
            messages.error(request, "Número, Tipo e Capacidade são obrigatórios!")
            return redirect('cadastrar_quarto', id=id)