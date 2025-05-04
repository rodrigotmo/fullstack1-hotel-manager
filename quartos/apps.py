from django.apps import AppConfig
from django.db.models.signals import post_migrate


class QuartosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quartos'
    def ready(self):
        post_migrate.connect(create_default_values, sender=self)


# Função que será chamada após as migrações
def create_default_values(sender, **kwargs):
    from .models import TipoQuarto, StatusQuarto
    TipoQuarto.create_default_values()
    StatusQuarto.create_default_values()