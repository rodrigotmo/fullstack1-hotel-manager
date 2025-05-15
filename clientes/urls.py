from django.urls import path
from clientes import views 

urlpatterns = [
    path('', views.clientes, name='clientes'), 
    path('cadastro', views.cadastrar_cliente, name='cadastrar_cliente'), 
    path('editar/<int:id>', views.editar_cliente, name='editar_cliente'), 
    path('desativar/<int:id>', views.desativar_cliente, name='desativar_cliente'), 
    path('ativar/<int:id>', views.ativar_cliente, name='ativar_cliente')
]