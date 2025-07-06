from django.contrib import admin
from django.urls import include, path
from principal import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.login, name='login'), 
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('home', views.home, name='home'), 
    
    path("funcionarios/", include("funcionarios.urls")),

    path("clientes/", include("clientes.urls")),

    path("quartos/", include("quartos.urls")),
    
    path("reservas/", include("reservas.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
