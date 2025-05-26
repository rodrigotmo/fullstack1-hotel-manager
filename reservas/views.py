from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from reservas.forms import ReservaForm
from reservas.models import Reserva, StatusReserva
from django.utils.timezone import now

@login_required
def reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reserva/reservas.html', {'reservas': reservas})

@login_required
def cadastrar_reserva(request):
    cliente_id = request.GET.get('cliente_id')
    cliente_inicial = None

    if cliente_id:
        try:
            cliente_inicial = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            cliente_inicial = None

    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva cadastrada com sucesso.')
            return redirect('reservas')
    else:
        form = ReservaForm(initial={'cliente': cliente_inicial}, user=request.user)

    return render(request, 'reserva/cadastro.html', {'form': form})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.status_reserva == StatusReserva.CANCELADA() or reserva.status_reserva == StatusReserva.FINALIZADA() or reserva.status_reserva == StatusReserva.EM_ANDAMENTO():
        messages.info(request, 'Esta reserva já está cancelada, finalizada ou em andamento.')
    else:
        reserva.status_reserva = StatusReserva.CANCELADA()
        reserva.data_cancelamento = now()
        reserva.save()
        messages.success(request, f'Reserva #{reserva.id} cancelada com sucesso.')

    return redirect('reservas')