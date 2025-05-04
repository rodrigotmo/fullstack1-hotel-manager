from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome