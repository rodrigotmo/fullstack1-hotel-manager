from django.contrib import admin
from django.urls import include, path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.login, name='login'), 
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('home', views.home, name='home'), 
    
    path("funcionarios/", include("funcionarios.urls")),

    path("quartos/", include("quartos.urls")),
    
    path("reservas/", include("reservas.urls")),
]
