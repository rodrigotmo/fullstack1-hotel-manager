from django.urls import path
from reservas import views 

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('cadastro', views.cadastrar_reserva, name='cadastrar_reserva'),
]