from django.urls import path
from funcionarios import views 

urlpatterns = [
    path('', views.funcionarios, name='funcionarios'), 
    path('ordenar/<campo>/', views.ordenar_funcionarios, name='ordenar_funcionarios'),
    path('cadastro', views.cadastrar_funcionario, name='cadastrar_funcionario'), 
    path('editar/<int:id>', views.editar_funcionario, name='editar_funcionario'), 
    path('desativar/<int:id>', views.desativar_funcionario, name='desativar_funcionario'), 
    path('ativar/<int:id>', views.ativar_funcionario, name='ativar_funcionario')
]