from django.urls import path
from reservas import views

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('cadastro/reserva_inicial', views.reserva_inicial, name='reserva_inicial'),
    path('cadastro/selecionar-quarto/', views.selecionar_quarto, name='selecionar_quarto'),
    path('cadastro/resumo/', views.resumo_reserva, name='resumo_reserva'),
    path('cadastro/limpar/', views.limpar_sessao_reserva, name='limpar_sessao_reserva'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
