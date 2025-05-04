from django.shortcuts import get_object_or_404, redirect, render
from principal.models import Reserva
from quartos.models import Quarto, TipoQuarto, StatusQuarto, Ocorrencia
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import now
from .forms import TipoQuartoForm, QuartoForm, OcorrenciaForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def quartos(request):
    if request.user.is_staff:
        quartos = Quarto.objects.exclude(status_quarto__nome_status_quarto='Removido').all()
        return render(request, 'quarto/quartos.html', {'quartos': quartos})
    else:
        messages.error(request, 'Você precisa estar logado como administrador para acessar esta página.')
        return redirect('home')
    
@login_required    
def cadastrar_quarto(request):
    if not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador.')
        return redirect('home')

    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            if Quarto.objects.filter(numero=numero).exists():
                messages.error(request, 'Quarto já cadastrado.')
                return redirect('quartos')
            quarto = form.save(commit=False)
            quarto.status_quarto_id = 1  # Liberado
            quarto.save()
            messages.success(request, 'Quarto cadastrado com sucesso.')
            return redirect('quartos')
    else:
        form = QuartoForm()
    return render(request, 'quarto/cadastro.html', {'form': form, 'quarto': None})
    
@login_required
def editar_quarto(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Você precisa estar logado com um usuário administrador.')
        return redirect('home')

    quarto = get_object_or_404(Quarto, id=id)
    if request.method == 'POST':
        form = QuartoForm(request.POST, instance=quarto)
        if form.is_valid():
            numero = form.cleaned_data['numero']
            if Quarto.objects.exclude(id=id).filter(numero=numero).exists():
                messages.error(request, 'Número de quarto já utilizado.')
                return redirect('editar_quarto', id=id)
            form.save()
            messages.success(request, 'Quarto atualizado com sucesso.')
            return redirect('quartos')
    else:
        form = QuartoForm(instance=quarto)
    return render(request, 'quarto/cadastro.html', {'form': form, 'quarto': quarto})

@login_required
def bloquear_liberar_quarto(request, id):
    if not request.user.is_staff:
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
        
@login_required        
def remover_quarto(request,id):
    if not request.user.is_staff:
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


@login_required
def tipos_quarto(request):
    if request.user.is_staff:
        tipos_quarto = TipoQuarto.objects.all()
        return render(request, 'tipo/tipos.html', {'tipos_quarto': tipos_quarto})
    else:
        messages.error(request, 'Você precisa estar logado como administrador para acessar esta página.')
        return redirect('home')

@login_required
def cadastrar_tipo_quarto(request):
    if not request.user.is_staff:
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


@login_required
def editar_tipo_quarto(request, id):
    if not request.user.is_staff:
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

@login_required
def ocorrencias(request):
    ocorrencias = Ocorrencia.objects.select_related('quarto').all().order_by('-data_abertura_ocorrencia')
    return render(request, 'ocorrencias/ocorrencias.html', {'ocorrencias': ocorrencias})

@login_required
def cadastrar_ocorrencia(request):
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            ocorrencia = form.save(commit=False)
            ocorrencia.data_abertura_ocorrencia = now()
            ocorrencia.finalizada = False
            ocorrencia.save()
            messages.success(request, 'Ocorrência registrada com sucesso.')
            return redirect('ocorrencias')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = OcorrenciaForm()
    return render(request, 'ocorrencias/cadastro.html', {'form': form})

@login_required
def finalizar_ocorrencia(request, id):
    ocorrencia = get_object_or_404(Ocorrencia, id=id)

    if ocorrencia.finalizada:
        messages.info(request, 'Esta ocorrência já está finalizada.')
    else:
        ocorrencia.finalizada = True
        ocorrencia.data_fechamento_ocorrencia = now()
        ocorrencia.save()
        messages.success(request, f'Ocorrência #{ocorrencia.id} finalizada com sucesso.')

    return redirect('ocorrencias')