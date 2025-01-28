from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Doador, Instituicao, Administrador, Doacao, Necessidade

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_doador', 'is_instituicao', 'is_admin')
    list_filter = ('is_doador', 'is_instituicao', 'is_admin')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('email',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doador', 'is_instituicao', 'is_admin')}),
    )

@admin.register(Doador)
class DoadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone')
    search_fields = ('usuario__username', 'usuario__email')

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'area_atuacao', 'contato')
    search_fields = ('usuario__username', 'usuario__email', 'area_atuacao')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario__username', 'usuario__email')

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('doador', 'descricao', 'categoria', 'estado_conservacao', 'status', 'data_criacao')
    list_filter = ('categoria', 'estado_conservacao', 'status')
    search_fields = ('descricao', 'doador__usuario__username')

    actions = ['marcar_como_doad']

    def marcar_como_doad(self, request, queryset):
        queryset.update(status='Doad')
    marcar_como_doad.short_description = "Marcar como doado"

@admin.register(Necessidade)
class NecessidadeAdmin(admin.ModelAdmin):
    list_display = ('instituicao', 'descricao', 'quantidade', 'data_criacao', 'aprovado_por_admin')
    list_filter = ('aprovado_por_admin',)
    search_fields = ('descricao', 'instituicao__usuario__username')
    actions = ['aprovar_necessidades']

    def aprovar_necessidades(self, request, queryset):
        queryset.update(aprovado_por_admin=True)
    aprovar_necessidades.short_description = "Aprovar necessidades selecionadas"
