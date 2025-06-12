from django.db import models
from funcionarios.models import Funcionario

# Create your models here.



class StatusQuarto(models.Model):
    nome_status_quarto = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_status_quarto

    @staticmethod
    def create_default_values():
        for status in ['Liberado', 'Em uso', 'Removido']:
            StatusQuarto.objects.get_or_create(nome_status_quarto=status)

    @classmethod
    def LIBERADO(cls):
        return cls.objects.get(nome_status_quarto='Liberado')

    @classmethod
    def EM_USO(cls):
        return cls.objects.get(nome_status_quarto='Em uso')

    @classmethod
    def REMOVIDO(cls):
        return cls.objects.get(nome_status_quarto='Removido')
 
class TipoQuarto(models.Model):
    nome_tipo_quarto = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_tipo_quarto
    
    @staticmethod
    def create_default_values():
        tipos = ['Simples', 'Duplo', 'Suite']
        for tipo in tipos:
            if not TipoQuarto.objects.filter(nome_tipo_quarto=tipo).exists():
                TipoQuarto.objects.create(nome_tipo_quarto=tipo)

class Quarto(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.RESTRICT)
    numero = models.CharField(max_length=10)
    capacidade = models.IntegerField()
    status_quarto = models.ForeignKey(StatusQuarto, on_delete=models.RESTRICT)
    reserva_liberada = models.BooleanField(default=True)

    def __str__(self):
        return f"Quarto {self.numero} - {self.tipo_quarto.nome_tipo_quarto}"


class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.RESTRICT)
    data_abertura_ocorrencia = models.DateTimeField()
    data_fechamento_ocorrencia = models.DateTimeField(null=True, blank=True)
    descricao = models.TextField()
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return f"Ocorrência no Quarto {self.quarto.numero}"
    
   


class TarifaTipoQuarto(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.RESTRICT)
    nome_tarifa_tipo_quarto = models.CharField(max_length=255)
    data_inicio_vigencia = models.DateField()
    data_fim_vigencia = models.DateField()
    valor_diaria = models.FloatField(default=0)

    def __str__(self):
        return f"{self.nome_tarifa_tipo_quarto} - R${self.valor_diaria}/dia"
    
    