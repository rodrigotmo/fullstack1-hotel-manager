from django.apps import AppConfig


class HotelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotelapp'
    def ready(self):
            from .models import TipoQuarto, StatusQuarto, StatusReserva
            TipoQuarto.create_default_values()
            StatusQuarto.create_default_values()
            StatusReserva.create_default_values()