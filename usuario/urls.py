from django.urls import path
from . import views

urlpatterns = [
    path('usuario/home', views.Home, name = 'usuariohome'),
    path('usuario/todos.eventos', views.todosEventos, name = 'usuariotodoseventos'),
    path('usuario/sobre', views.Sobre, name = 'usuariosobre'),
    path('usuario/desc_evento/<int:id>', views.descEvento, name = 'usuariodesc_evento'),
    path('usuario/adquirir_voucher/<int:id>', views.adquirirVoucher, name = 'usuarioadquirir_voucher'),
    path('usuario/voucher/<int:id>', views.verVoucher, name = 'usuariover_voucher'),
    path('usuario/adicionar_evento', views.adicionarEvento, name = 'usuarioadicionar_evento'),
    path('usuario/editar_evento/<int:id>', views.editarEvento, name = 'usuarioeditar_evento'),
    path('usuario/deletar_evento/<int:id>', views.deletarEvento, name = 'usuariodeletar_evento'),
]