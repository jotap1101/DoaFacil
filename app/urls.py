from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doacoes/', views.doacoes_view, name='doacoes'),
    path('doacoes/<int:doacao_id>/', views.buscar_dados_doacao, name='realizar_doacao'),
    path('doacoes/cadastrar-doacao/', views.cadastrar_doacao, name='cadastrar_doacao'),
    path('doacoes/<int:doacao_id>/detalhar-doacao', views.detalhar_doacao, name='detalhar_doacao'),
    path('doacoes/<int:doacao_id>/editar-doacao/', views.editar_doacao, name='editar_doacao'),
    path('doacoes/<int:doacao_id>/excluir-doacao/', views.excluir_doacao, name='excluir_doacao'),
    path('necessidades/', views.necessidades_view, name='necessidades'),
    path('necessidades/<int:necessidade_id>/', views.buscar_dados_necessidade, name='realizar_doacao'),
    path('necessidades/cadastrar-necessidade/', views.cadastrar_necessidade, name='cadastrar_necessidade'),
    path('necessidades/<int:necessidade_id>/detalhar-necessidade', views.detalhar_necessidade, name='detalhar_necessidade'),
    path('necessidades/<int:necessidade_id>/editar-necessidade/', views.editar_necessidade, name='editar_necessidade'),
    path('necessidades/<int:necessidade_id>/excluir-necessidade/', views.excluir_necessidade, name='excluir_necessidade'),
    path('cadastrar-item/', views.cadastrar_item, name='cadastrar_item'),
]