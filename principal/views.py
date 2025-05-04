from django.shortcuts import redirect, render
from reservas.models import Reserva, StatusReserva
from clientes.models import Cliente
from funcionarios.models import Funcionario
from quartos.models import Quarto, StatusQuarto, Ocorrencia
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            funcionario = authenticate(request, username=usuario, password=senha)
            if funcionario is not None and funcionario.ativo:
                auth_login(request, funcionario)
                messages.success(request, f'Bem-vindo(a), {funcionario.username}')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'login.html', {'form': form})
     
@login_required     
def logout(request):
    auth_logout(request)
    return redirect('login')
      
@login_required      
def home(request):
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

    
