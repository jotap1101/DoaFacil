from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('doacoes/', views.listar_doacoes, name='listar_doacoes'),  # Lista de doações
    path('instituicoes/', views.listar_instituicoes, name='listar_instituicoes'),  # Lista de instituições
    path('necessidades/', views.listar_necessidades, name='listar_necessidades'),  # Lista de necessidades
    path('doacoes/<int:doacao_id>/', views.detalhes_doacao, name='detalhes_doacao'),  # Detalhes de uma doação
    path('instituicoes/<int:instituicao_id>/', views.detalhes_instituicao, name='detalhes_instituicao'),  # Detalhes de uma instituição
    path('cadastrar_doacao/', views.cadastrar_doacao, name='cadastrar_doacao'),  # Cadastro de doação
    path('cadastrar_necessidade/', views.cadastrar_necessidade, name='cadastrar_necessidade'),  # Cadastro de necessidade
    path('register/', views.register_view, name='register'),
    path('pagdoacoes', views.DoacoesView, name='pagdoacoes'),
    # path('instituicoes', views.InstituicoesView, name='instituicoes'),
    # path('areasdosaber', views.AreasdosaberView, name='areasdosaber'),
]