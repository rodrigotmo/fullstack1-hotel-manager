from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


# Gerenciador de Usuários Personalizado
class FuncionarioManager(BaseUserManager):
    def create_user(self, username, password, nome, is_staff, **extra_fields):
        if not username:
            raise ValueError('O username é obrigatório')
        if not password:
            raise ValueError('A senha é obrigatória')
        
        funcionario = self.model(
            username=username,
            nome=nome,
            ativo=True,
            is_staff=is_staff,
            **extra_fields
        )
        funcionario.set_password(password)  # Criptografa a senha
        funcionario.save(using=self._db)
        return funcionario

    def create_superuser(self, username, password, nome, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, password, nome, **extra_fields)


# Modelo de Funcionario
class Funcionario(AbstractBaseUser):
    nome = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = FuncionarioManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['nome'] 

    def __str__(self):
        return self.nome
    
    def buscar_nome(self):
        return self.nome
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    def has_perm(self, app_label):
        return self.is_staff



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


class StatusQuarto(models.Model):
    nome_status_quarto = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_status_quarto
    
    @staticmethod
    def create_default_values():
        statuses = ['Liberado', 'Em uso', 'Indisponível', 'Removido']
        for status in statuses:
            if not StatusQuarto.objects.filter(nome_status_quarto=status).exists():
                StatusQuarto.objects.create(nome_status_quarto=status)


class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class TarifaTipoQuarto(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.CASCADE)
    nome_tarifa_tipo_quarto = models.CharField(max_length=255)
    data_inicio_vigencia = models.DateField()
    data_fim_vigencia = models.DateField()
    valor_diaria = models.FloatField(default=0)

    def __str__(self):
        return self.nome_tarifa_tipo_quarto


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


class Quarto(models.Model):
    tipo_quarto = models.ForeignKey(TipoQuarto, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    capacidade = models.IntegerField()
    status_quarto = models.ForeignKey(StatusQuarto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Quarto {self.numero}"


class Ocorrencia(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE)
    data_abertura_ocorrencia = models.DateField()
    data_fechamento_ocorrencia = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return f"Ocorrência no Quarto {self.quarto.numero}"


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