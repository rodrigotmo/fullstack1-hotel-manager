from django.urls import path
from quartos import views 

urlpatterns = [
    path('', views.quartos, name='quartos'), 
    path('cadastro', views.cadastrar_quarto, name='cadastrar_quarto'), 
    path('editar/<int:id>', views.editar_quarto, name='editar_quarto'), 
    path('remover/<int:id>', views.remover_quarto, name='remover_quarto'), 
    path('bloquear/<int:id>', views.bloquear_liberar_quarto, name='bloquear_quarto'), 
    path('liberar/<int:id>', views.bloquear_liberar_quarto, name='liberar_quarto'), 
    
    path('tipos', views.tipos_quarto, name='tipos_quarto'), 
    path('tipos/cadastro', views.cadastrar_tipo_quarto, name='cadastrar_tipo_quarto'), 
    path('tipos/editar/<int:id>', views.editar_tipo_quarto, name='editar_tipo_quarto'), 
    
    path('ocorrencias', views.ocorrencias, name='ocorrencias'),    
    path('ocorrencias/cadastro', views.cadastrar_ocorrencia, name='cadastrar_ocorrencia'),
    path('ocorrencias/finalizar/<int:id>', views.finalizar_ocorrencia, name='finalizar_ocorrencia'),
    
    path('tarifas', views.tarifas, name='tarifas'),    
    path('tarifas/cadastro', views.cadastrar_tarifa, name='cadastrar_tarifa'),
    path('tarifas/editar/<int:id>', views.editar_tarifa, name='editar_tarifa'),
]