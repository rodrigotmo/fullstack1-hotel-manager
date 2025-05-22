from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from reservas.forms import ReservaForm
from reservas.models import Reserva

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