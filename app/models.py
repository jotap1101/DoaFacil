from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta

class Usuario(AbstractUser):
    """Usuário base para doadores, instituições e administradores."""
    email = models.EmailField(unique=True)
    is_doador = models.BooleanField(default=False)
    is_instituicao = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="+",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="+",
        blank=True,
        help_text="Specific permissions for this user.",
    )

class Doador(models.Model):
    """Doador pode cadastrar doações."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)

class Instituicao(models.Model):
    """Instituição pode registrar necessidades."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    area_atuacao = models.CharField(max_length=100)
    contato = models.CharField(max_length=100)

    def total_necessidades_semanais(self):
        """Retorna o número de necessidades registradas na última semana."""
        uma_semana_atras = now() - timedelta(weeks=1)
        return self.necessidade_set.filter(data_criacao__gte=uma_semana_atras).count()
    
    def pode_registrar_necessidade(self):
        """Verifica se a instituição pode registrar uma nova necessidade."""
        return self.total_necessidades_semanais() < 10

class Administrador(models.Model):
    """Administrador pode gerenciar o sistema."""
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

class Doacao(models.Model):
    """Modelo para cadastro de doações."""
    doador = models.ForeignKey('Doador', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)  # Campo adicionado
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)
    estado_conservacao = models.CharField(  # Campo adicionado
        max_length=20,
        choices=[
            ('Novo', 'Novo'),
            ('Usado', 'Usado'),
            ('Bom', 'Bom'),
            ('Ruim', 'Ruim'),
        ],
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('Disponível', 'Disponível'),
            ('Doad', 'Doad'),
        ],
        default='Disponível',
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def marcar_como_doad(self):
        """Marca a doação como realizada."""
        self.status = 'Doad'
        self.save()

class Necessidade(models.Model):
    """Modelo para cadastro de necessidades de uma instituição."""
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado_por_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Valida a regra de negócio antes de salvar uma nova necessidade."""
        if not self.aprovado_por_admin and not self.instituicao.pode_registrar_necessidade():
            raise ValueError("Limite de necessidades semanais atingido. Contate um administrador.")
        super().save(*args, **kwargs)
