from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doacoes/', views.doacoes_view, name='doacoes'),
    path('cadastrar-doacao/', views.cadastrar_doacao, name='cadastrar_doacao'),
    path('editar-doacao/<int:doacao_id>/', views.editar_doacao, name='editar_doacao'),
    path('doacoes/<int:doacao_id>/', views.detalhes_doacao, name='detalhes_doacao'),
    path('necessidades/', views.necessidades_view, name='necessidades'),
    path('cadastrar-necessidade/', views.cadastrar_necessidade, name='cadastrar_necessidade'),
    path('cadastrar-item/', views.cadastrar_item, name='cadastrar_item'),
]