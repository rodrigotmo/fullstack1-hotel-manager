from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from reservas.forms import ReservaForm
from reservas.models import Reserva

@login_required
def reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reserva/reservas.html', {'reservas': reservas})

@login_required
def cadastrar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva cadastrada com sucesso.')
            return redirect('reservas')
    else:
        form = ReservaForm(user=request.user)

    return render(request, 'reserva/cadastro.html', {'form': form})