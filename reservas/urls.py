from django.urls import path
from reservas import views 

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('cadastro', views.cadastrar_reserva, name='cadastrar_reserva'),
    path('cancelar/<int:reserva_id>', views.cancelar_reserva, name='cancelar_reserva'),
]