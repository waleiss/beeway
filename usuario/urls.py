from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login, name = 'login'),
    path('cadastro', views.Cadastro, name = 'cadastro'),
    path('rSenha', views.rSenha, name = 'rSenha'),
    path('home', views.Home, name = 'home'),
    path('todos.eventos', views.todosEventos, name = 'todoseventos'),
    path('sobre', views.Sobre, name = 'sobre'),
    path('desc_evento', views.descEvento, name = 'desc_evento'),
    path('voucher', views.Voucher, name = 'voucher'),
]
