from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from principal.models import Reserva, Cliente, StatusReserva
from funcionarios.models import Funcionario
from quartos.models import Quarto, StatusQuarto, Ocorrencia
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db.models import Q

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
    
