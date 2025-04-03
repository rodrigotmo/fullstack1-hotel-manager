from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
