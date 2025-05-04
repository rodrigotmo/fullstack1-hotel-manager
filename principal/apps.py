from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PrincipalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'principal'
    def ready(self):
        post_migrate.connect(create_default_values, sender=self)


# Função que será chamada após as migrações
def create_default_values(sender, **kwargs):
    from .models import StatusReserva
    StatusReserva.create_default_values()