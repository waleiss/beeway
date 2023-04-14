from django.urls import path
from . import views

urlpatterns = [
    path('administrador/home', views.Home, name = 'adminhome'),
    path('administrador/todos.eventos', views.todosEventos, name = 'admintodoseventos'),
    path('administrador/sobre', views.Sobre, name = 'adminsobre'),
    path('administrador/desc_evento/<int:id>', views.descEvento, name = 'admindesc_evento'),
    path('administrador/voucher', views.Voucher, name = 'adminvoucher'),
    path('administrador/adicionar_evento', views.adicionarEvento, name = 'adminadicionar_evento'),
    path('administrador/editar_evento/<int:id>', views.editarEvento, name = 'admineditar_evento'),
]
