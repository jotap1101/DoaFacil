from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import*

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos que devem ser exibidos na listagem de usuários
    list_display = ('username', 'email', 'tipo_usuario', 'is_staff', 'is_active', 'date_joined')
    
    # Campos que devem ser exibidos ao adicionar ou editar um usuário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'tipo_usuario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que aparecerão no formulário de criação/edição de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'tipo_usuario', 'is_staff', 'is_active'),
        }),
    )

    # Registra a classe UsuarioAdmin
    search_fields = ('username', 'email')
    ordering=('username',)
    
@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Mostra o ID e o nome na lista de itens
    search_fields = ('nome',)  # Adiciona um campo de busca por nome
    ordering = ('nome',)  # Ordena os tipos de usuário em ordem alfabética

class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('nome',)  # Exibe o nome da categoria na lista
    search_fields = ('nome',)  # Permite buscar pela categoria
    ordering = ('nome',)  # Ordena por nome


# Classe admin para Item
class ItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'descricao', 'data_disponibilidade', 'status')  # Campos a exibir na lista
    search_fields = ('usuario_username', 'categoria_nome', 'descricao')  # Permite buscar por usuário, categoria e descrição
    list_filter = ('status', 'categoria')  # Filtros de status e categoria
    ordering = ('data_disponibilidade',)  # Ordena pela data de disponibilidade


# Classe admin para Doacao
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'item', 'estado_conservacao', 'status', 'data_doacao')  # Campos a exibir na lista
    search_fields = ('usuario_username', 'item_descricao', 'estado_conservacao')  # Permite buscar por usuário, item e estado
    list_filter = ('estado_conservacao', 'status')  # Filtros de estado de conservação e status
    ordering = ('data_doacao',)  # Ordena pela data de doação


# Classe admin para Necessidade
class NecessidadeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'item', 'quantidade', 'aprovado_por_admin', 'status', 'data_necessidade')  # Campos a exibir na lista
    search_fields = ('usuario_username', 'item_descricao', 'quantidade')  # Permite buscar por usuário, item e quantidade
    list_filter = ('status', 'aprovado_por_admin')  # Filtros de status e aprovado por admin
    ordering = ('data_necessidade',)  # Ordena pela data de necessidade


# Registro dos modelos e suas respectivas classes admin
admin.site.register(CategoriaItem, CategoriaItemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Doacao, DoacaoAdmin)
admin.site.register(Necessidade, NecessidadeAdmin)