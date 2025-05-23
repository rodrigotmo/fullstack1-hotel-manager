from django.db import models
from funcionarios.models import Funcionario
from quartos.models import Quarto, TarifaTipoQuarto
from clientes.models import Cliente

# Create your models here.
class StatusReserva(models.Model):
    nome_status_reserva = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_status_reserva
    
    @staticmethod
    def create_default_values():
        # Adicionando valores padrão
        statuses = ['Reservada', 'Em andamento', 'Finalizada', 'Cancelada']
        for status in statuses:
            if not StatusReserva.objects.filter(nome_status_reserva=status).exists():
                StatusReserva.objects.create(nome_status_reserva=status)
    @classmethod
    def RESERVADA(cls):
        return cls.objects.get(nome_status_reserva='Reservada')

    @classmethod
    def EM_ANDAMENTO(cls):
        return cls.objects.get(nome_status_reserva='Em andamento')

    @classmethod
    def FINALIZADA(cls):
        return cls.objects.get(nome_status_reserva='Finalizada')

    @classmethod
    def CANCELADA(cls):
        return cls.objects.get(nome_status_reserva='Cancelada')


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    status_reserva = models.ForeignKey(StatusReserva, on_delete=models.RESTRICT)
    tarifa_tipo_quarto = models.ForeignKey(TarifaTipoQuarto, on_delete=models.RESTRICT)
    data_reserva_criada = models.DateField()
    data_reserva_previsao_inicio = models.DateField()
    data_reserva_previsao_fim = models.DateField()
    data_check_in = models.DateField(blank=True, null=True)
    data_check_out = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-data_reserva_criada']

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nome}"