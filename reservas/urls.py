from django.urls import path
from reservas import views

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('canceladas/', views.reservas_canceladas, name='reservas_canceladas'),
    path('finalizadas/', views.reservas_finalizadas, name='reservas_finalizadas'),

    path('reservas/checkin/<int:reserva_id>/', views.checkin, name='checkin'),
    path('reservas/checkout/<int:reserva_id>/', views.checkout, name='checkout'),

    path('cadastro/reserva_inicial', views.reserva_inicial, name='reserva_inicial'),
    path('cadastro/selecionar-quarto/', views.selecionar_quarto, name='selecionar_quarto'),
    path('cadastro/resumo/', views.resumo_reserva, name='resumo_reserva'),
    path('cadastro/limpar/', views.limpar_sessao_reserva, name='limpar_sessao_reserva'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    
    path('relatorios/', views.relatorios_reservas, name='relatorios_reservas'),
    path('relatorios/ativas', views.relatorio_reservas_ativas, name='relatorio_reservas_ativas'),
    path('relatorios/finalizadas', views.relatorio_reservas_finalizadas, name='relatorio_reservas_finalizadas'),
    path('relatorios/canceladas', views.relatorio_reservas_canceladas, name='relatorio_reservas_canceladas'),
]
