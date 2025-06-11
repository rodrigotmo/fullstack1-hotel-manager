from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from clientes.models import Cliente
from quartos.models import Quarto, StatusQuarto, TarifaTipoQuarto
from reservas.models import Reserva, StatusReserva
from reservas.forms import ReservaInicialForm
from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone

@login_required
def reservas(request):
    ordenacao_personalizada = Case(
        When(status_reserva=StatusReserva.EM_ANDAMENTO(), then=Value(0)),
        When(status_reserva=StatusReserva.RESERVADA(), then=Value(1)),
        default=Value(2),
        output_field=IntegerField()
    )
    reservas = Reserva.objects.filter(
        status_reserva__in=[StatusReserva.EM_ANDAMENTO(), StatusReserva.RESERVADA()]
    ).annotate(
        ordem_status=ordenacao_personalizada
    ).order_by('ordem_status', '-data_reserva_criada')
    return render(request, 'reserva/reservas.html', {'reservas': reservas})

@login_required
def reserva_inicial(request):
            
    if request.method == 'POST':
        form = ReservaInicialForm(request.POST)
        if form.is_valid():
            request.session['reserva_dados'] = {
                'cliente_id': form.cleaned_data['cliente'].id,
                'data_inicio': form.cleaned_data['data_reserva_previsao_inicio'].isoformat(),
                'data_fim': form.cleaned_data['data_reserva_previsao_fim'].isoformat(),
            }
            return redirect('selecionar_quarto')
    else:
        dados = request.session.get('reserva_dados')
        initial = {}
        if dados or request.GET.get('cliente_id'):
            if dados:
                initial['cliente'] = dados.get('cliente_id')
                initial['data_reserva_previsao_inicio'] = dados.get('data_inicio')
                initial['data_reserva_previsao_fim'] = dados.get('data_fim')
            else:
                cliente_id = request.GET.get('cliente_id')
                initial['cliente'] = cliente_id
        form = ReservaInicialForm(initial=initial)

    return render(request, 'reserva/reserva_inicial.html', {'form': form})

@login_required
def limpar_sessao_reserva(request):
    if 'reserva_dados' in request.session:
        del request.session['reserva_dados']
    return redirect('reserva_inicial')

@login_required
def selecionar_quarto(request):
    dados = request.session.get('reserva_dados')
    if not dados:
        messages.error(request, "Dados da reserva não encontrados. Por favor, preencha o formulário inicial.")
        return redirect('reserva_inicial')

    cliente_id = dados['cliente_id']
    cliente = get_object_or_404(Cliente, id=cliente_id)
    data_inicio = dados['data_inicio']
    data_fim = dados['data_fim']
    data_inicio_formatado = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    data_fim_formatado = datetime.strptime(data_fim, '%Y-%m-%d').date()
    qtd_dias = (data_fim_formatado - data_inicio_formatado).days
    

    quartos_base = Quarto.objects.exclude(
        status_quarto=StatusQuarto.REMOVIDO()
    ).filter(reserva_liberada=True)


    quartos_ocupados = Reserva.objects.filter(
        data_reserva_previsao_inicio__lt=data_fim,
        data_reserva_previsao_fim__gt=data_inicio
    ).exclude(
        status_reserva__in=[StatusReserva.CANCELADA(), StatusReserva.FINALIZADA()]
    ).values_list('quarto_id', flat=True)

    quartos_disponiveis = quartos_base.exclude(id__in=quartos_ocupados)

    quartos_com_tarifa = []
    for quarto in quartos_disponiveis:
        tarifa = TarifaTipoQuarto.objects.filter(
            tipo_quarto=quarto.tipo_quarto,
            data_inicio_vigencia__lte=data_inicio,
            data_fim_vigencia__gte=data_fim
        ).first()
        if tarifa:
            quartos_com_tarifa.append({
                'quarto': quarto,
                'tarifa': tarifa,
            })

    if request.method == 'POST':
        quarto_id = request.POST.get('quarto_id')
        if not quarto_id:
            messages.error(request, "Por favor, selecione um quarto.")
        else:
            try:
                quarto_selecionado = quartos_disponiveis.get(id=quarto_id)
            except Quarto.DoesNotExist:
                messages.error(request, "Quarto inválido ou indisponível.")
                return redirect('selecionar_quarto')
            dados = request.session.get('reserva_dados', {})
            dados['quarto_id'] = quarto_selecionado.id
            request.session['reserva_dados'] = dados
            request.session.modified = True

            return redirect('resumo_reserva')

    return render(request, 'reserva/selecionar_quarto.html', {
        'quartos_com_tarifa': quartos_com_tarifa,
        'cliente': cliente,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'qtd_dias': qtd_dias,
    })

@login_required
def resumo_reserva(request):
    dados = request.session.get('reserva_dados')
    if not dados or 'quarto_id' not in dados:
        messages.error(request, "Dados incompletos da reserva. Por favor, inicie novamente.")
        return redirect('reserva_inicial')

    cliente_id = dados['cliente_id']
    data_inicio = dados['data_inicio']
    data_fim = dados['data_fim']
    data_inicio_formatado = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    data_fim_formatado = datetime.strptime(data_fim, '%Y-%m-%d').date()
    qtd_dias = (data_fim_formatado - data_inicio_formatado).days
    quarto_id = dados['quarto_id']

    cliente = get_object_or_404(Cliente, id=cliente_id)
    quarto = get_object_or_404(Quarto, id=quarto_id)

    tarifa = TarifaTipoQuarto.objects.filter(
        tipo_quarto=quarto.tipo_quarto,
        data_inicio_vigencia__lte=data_inicio,
        data_fim_vigencia__gte=data_fim
    ).first()

    if not tarifa:
        messages.error(request, "Não há tarifa definida para o quarto selecionado nas datas escolhidas.")
        return redirect('selecionar_quarto')

    if request.method == 'POST':
        reserva = Reserva(
            cliente=cliente,
            funcionario=request.user,
            quarto=quarto,
            status_reserva=StatusReserva.RESERVADA(),
            tarifa_tipo_quarto=tarifa,
            data_reserva_previsao_inicio=data_inicio,
            data_reserva_previsao_fim=data_fim,
        )
        reserva.save()
        messages.success(request, f"Reserva criada com sucesso para o quarto {quarto.numero}.")
        if 'reserva_dados' in request.session:
            del request.session['reserva_dados']
        return redirect('reservas')

    return render(request, 'reserva/resumo_reserva.html', {
        'cliente': cliente,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'quarto': quarto,
        'tarifa': tarifa,
        'qtd_dias': qtd_dias,
    })

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.status_reserva in [StatusReserva.CANCELADA(), StatusReserva.FINALIZADA(), StatusReserva.EM_ANDAMENTO()]:
        messages.info(request, 'Esta reserva já está cancelada, finalizada ou em andamento.')
    else:
        reserva.status_reserva = StatusReserva.CANCELADA()
        reserva.data_cancelamento = now()
        reserva.save()
        messages.success(request, f'Reserva #{reserva.id} cancelada com sucesso.')

    return redirect('reservas')

@login_required
def checkin(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.status_reserva != StatusReserva.RESERVADA():
        messages.error(request, 'Esta reserva não está mais disponível para check-in.')
        return redirect('reservas')
    
    quarto = reserva.quarto
    if quarto.status_quarto != StatusQuarto.LIBERADO():
        messages.error(request, 'O quarto selecionado não está disponível para check-in.')
        return redirect('reservas')

    reserva.status_reserva = StatusReserva.EM_ANDAMENTO()
    reserva.data_check_in = timezone.now()
    reserva.save()

    quarto.status_quarto = StatusQuarto.EM_USO()
    quarto.save()

    messages.success(request, f'Check-in realizado com sucesso para a reserva #{reserva.id}.')
    
    return redirect('reservas')

@login_required
def checkout(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.status_reserva != StatusReserva.EM_ANDAMENTO():
        messages.error(request, 'Esta reserva não está em andamento para checkout.')
        return redirect('reservas')

    reserva.status_reserva = StatusReserva.FINALIZADA()
    reserva.data_check_out = timezone.now()
    reserva.save()

    quarto = reserva.quarto
    quarto.status_quarto = StatusQuarto.LIBERADO()
    quarto.save()

    messages.success(request, f'Checkout realizado com sucesso para a reserva #{reserva.id}.')
    
    return redirect('reservas')