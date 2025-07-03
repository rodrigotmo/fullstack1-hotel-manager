from django.contrib import admin
from .models import Reserva, StatusReserva

# Register your models here.
admin.site.register(Reserva)
admin.site.register(StatusReserva)