from django.urls import path
from . import views

urlpatterns = [
    path('usuario/home', views.Home, name = 'usuariohome'),
    path('usuario/todos.eventos', views.todosEventos, name = 'usuariotodoseventos'),
    path('usuario/sobre', views.Sobre, name = 'usuariosobre'),
    path('usuario/desc_evento/<int:id>', views.descEvento, name = 'usuariodesc_evento'),
    path('usuario/adquirir_voucher/<int:id>', views.adquirirVoucher, name = 'usuarioadquirir_voucher'),
    path('usuario/voucher', views.viewVoucher, name = 'usuariovoucher'),
]