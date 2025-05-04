from django.db import models
from funcionarios.models import Funcionario
from quartos.models import Quarto, TarifaTipoQuarto



class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome



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


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    status_reserva = models.ForeignKey(StatusReserva, on_delete=models.CASCADE)
    tarifa_tipo_quarto = models.ForeignKey(TarifaTipoQuarto, on_delete=models.CASCADE)
    data_reserva = models.DateField()
    data_check_in = models.DateField()
    data_check_out = models.DateField()

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nome}"