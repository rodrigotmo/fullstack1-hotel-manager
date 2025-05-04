from django.urls import path
from reservas import views 

urlpatterns = [
    path('', views.reservas, name='reservas'), 
]