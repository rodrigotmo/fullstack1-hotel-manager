from django.shortcuts import get_object_or_404, redirect, render
from principal.models import Reserva
from quartos.models import Quarto, TipoQuarto, StatusQuarto
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db.models import Q
from .forms import TipoQuartoForm

# Create your views here.

def quartos(request):
    if request.user.is_authenticated and request.user.is_staff:
        quartos = Quarto.objects.exclude(status_quarto__nome_status_quarto='Removido').all()
        return render(request, 'quarto/quartos.html', {'quartos': quartos})
    else:
        messages.error(request, 'Você precisa estar logado como administrador para acessar esta página.')
        return redirect('home')
    
def cadastrar_quarto(request):
    if not request.user.is_authenticated and request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    if request.method == 'GET':
        tipos_quarto = TipoQuarto.objects.all()
        return render(request, 'quarto/cadastro.html', {'tipos_quarto': tipos_quarto, 'quarto': None})
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
        return render(request, 'quarto/cadastro.html', {'quarto': quarto, 'tipos_quarto': tipos_quarto})
    
    elif request.method == 'POST':
        numero = request.POST.get('numero')
        capacidade = request.POST.get('capacidade')
        tipo = request.POST.get('tipo_quarto')
        outro_quarto = Quarto.objects.exclude(id=id).filter(numero=numero).first()
        if numero and capacidade and tipo and outro_quarto is None:
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
            messages.error(request, "Número deve ser único, Tipo e Capacidade são obrigatórios!")
            return redirect('editar_quarto', id=id)
  
def bloquear_liberar_quarto(request, id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    quarto = get_object_or_404(Quarto, id=id) 
    reservas = Reserva.objects.filter(Q(quarto_id=quarto) & (Q(status_reserva__nome_status_reserva='Reservada') | Q(status_reserva__nome_status_reserva='Em andamento'))).first()
    if reservas:
        messages.error(request, 'Status do quarto não pode ser mudado pois possui reservas ativas.')
        return redirect('quartos')
    else:
        if quarto.status_quarto.nome_status_quarto == 'Indisponível':
            quarto.status_quarto = StatusQuarto.objects.get(nome_status_quarto='Liberado')
        else:
            quarto.status_quarto = StatusQuarto.objects.get(nome_status_quarto='Indisponível')
            
        quarto.save()
        messages.success(request, quarto.status_quarto)
        messages.success(request, 'Status do quarto alterado com sucesso.')
        return redirect('quartos')
        
def remover_quarto(request,id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')
    
    quarto = get_object_or_404(Quarto, id=id)
    reservas = Reserva.objects.filter(Q(quarto_id=quarto) & (Q(status_reserva__nome_status_reserva='Reservada') | Q(status_reserva__nome_status_reserva='Em andamento'))).first()
    if reservas:
        messages.error(request, 'Quarto não pode ser removido, pois possui reservas ativas.')
        return redirect('quartos')
    else:
        quarto.status_quarto = StatusQuarto.objects.get(nome_status_quarto='Removido')
        quarto.numero = quarto.numero + ' - Removido'
        quarto.save()
        messages.success(request, 'Quarto removido com sucesso.')
        return redirect('quartos')



def tipos_quarto(request):
    if request.user.is_authenticated and request.user.is_staff:
        tipos_quarto = TipoQuarto.objects.all()
        return render(request, 'tipo/tipos.html', {'tipos_quarto': tipos_quarto})
    else:
        messages.error(request, 'Você precisa estar logado como administrador para acessar esta página.')
        return redirect('home')

def cadastrar_tipo_quarto(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

    if request.method == 'POST':
        form = TipoQuartoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome_tipo_quarto']
            if TipoQuarto.objects.filter(nome_tipo_quarto=nome).exists():
                messages.error(request, 'Tipo de Quarto já cadastrado.')
                return redirect('tipos_quarto')
            form.save()
            messages.success(request, 'Tipo de Quarto cadastrado com sucesso.')
            return redirect('tipos_quarto')
    else:
        form = TipoQuartoForm()

    return render(request, 'tipo/cadastro.html', {'form': form, 'tipo_quarto': None})


def editar_tipo_quarto(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador para acessar esta página.')
        return redirect('home')

    tipo_quarto = get_object_or_404(TipoQuarto, Q(id=id) & ~Q(nome_tipo_quarto__in=['Simples', 'Duplo', 'Suite']))

    if request.method == 'POST':
        form = TipoQuartoForm(request.POST, instance=tipo_quarto)
        if form.is_valid():
            nome = form.cleaned_data['nome_tipo_quarto']
            if TipoQuarto.objects.exclude(id=tipo_quarto.id).filter(nome_tipo_quarto=nome).exists():
                messages.error(request, 'Tipo de Quarto já cadastrado.')
                return redirect('editar_tipo_quarto', id=tipo_quarto.id)
            form.save()
            messages.success(request, 'Tipo de Quarto alterado com sucesso.')
            return redirect('tipos_quarto')
    else:
        form = TipoQuartoForm(instance=tipo_quarto)

    return render(request, 'tipo/cadastro.html', {'form': form, 'tipo_quarto': tipo_quarto})