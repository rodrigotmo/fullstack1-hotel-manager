from django.contrib import admin

from .models import Ocorrencia,StatusQuarto, Quarto, TipoQuarto, TarifaTipoQuarto
# Register your models here.
admin.site.register(Ocorrencia)
admin.site.register(StatusQuarto)
admin.site.register(TipoQuarto)
admin.site.register(TarifaTipoQuarto)
admin.site.register(Quarto)