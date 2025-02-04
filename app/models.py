from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, tipo_usuario=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, tipo_usuario=tipo_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, tipo_usuario=None, **extra_fields):
        tipo_usuario, created = TipoUsuario.objects.get_or_create(nome="Administrador")
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, tipo_usuario=tipo_usuario,**extra_fields)

class TipoUsuario(models.Model):
    class Meta:
        verbose_name = "Tipo de usuário"
        verbose_name_plural = "Tipos de usuários"

    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome")

    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, verbose_name="Tipo de usuário")
    telefone = models.CharField(max_length=11, null=True, blank=True, verbose_name='Telefone')
    objects = UsuarioManager()

    def __str__(self):
        return self.username
    
class CategoriaItem(models.Model):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome")

    def __str__(self):
        return self.nome    
    
class Item(models.Model):   
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"

    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Doado', 'Doado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='itens', verbose_name="Usuário")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    categoria = models.ForeignKey(CategoriaItem, on_delete=models.CASCADE, verbose_name="Categoria")
    descricao = models.TextField(verbose_name="Descrição")
    data_disponibilidade = models.DateTimeField(auto_now_add=True, verbose_name="Data de disponibilidade")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível', verbose_name="Status")

    def __str__(self):
        return self.nome

class Doacao(models.Model):
    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"

    ESTADO_CONSERVACAO_CHOICES = [
        ('Novo', 'Novo'),
        ('Usado', 'Usado'),
        ('Bom', 'Bom'),
        ('Ruim', 'Ruim'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='doacoes', verbose_name="Usuário")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    descricao = models.TextField(verbose_name="Descrição")
    estado_conservacao = models.CharField(max_length=20, choices=ESTADO_CONSERVACAO_CHOICES, verbose_name="Estado de conservação")
    status = models.CharField(max_length=20, choices=Item.STATUS_CHOICES, default='Disponível', verbose_name="Status")
    data_doacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de doação")

    def __str__(self):
        return f"{self.usuario} - {self.item}"

class Necessidade(models.Model):
    class Meta:
        verbose_name = "Necessidade"
        verbose_name_plural = "Necessidades"

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='necessidades', verbose_name="Usuário")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Item")
    descricao = models.TextField(verbose_name="Descrição")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    aprovado_por_admin = models.BooleanField(default=False, verbose_name="Aprovado por administrador")
    status = models.CharField(max_length=20, choices=Item.STATUS_CHOICES, default='Disponível', verbose_name="Status")
    data_necessidade = models.DateTimeField(auto_now_add=True, verbose_name="Data de necessidade")

    def __str__(self):
        return f"{self.usuario} - {self.item} - {self.quantidade}"