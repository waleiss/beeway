from django.urls import path
from . import views

urlpatterns = [
    path('home', views.Home, name = 'home'),
    path('todos.eventos', views.todosEventos, name = 'todoseventos'),
    path('sobre', views.Sobre, name = 'sobre'),
    path('desc_evento/<int:id>', views.descEvento, name = 'desc_evento'),
    path('adquirir_voucher/<int:id>', views.adquirirVoucher, name = 'adquirir_voucher'),
    path('voucher/<int:id>', views.verVoucher, name = 'ver_voucher'),
    path('meus.eventos', views.meusEventos, name = 'meuseventos'),
    path('adicionar_evento', views.adicionarEvento, name = 'adicionar_evento'),
    path('editar_evento/<int:id>', views.editarEvento, name = 'editar_evento'),
    path('deletar_evento/<int:id>', views.deletarEvento, name = 'deletar_evento'),
    path('meus.vouchers', views.meusVouchers, name = 'meusvouchers'),
    path('perfil', views.Perfil, name = 'meuperfil'),
    path('eventos.encerrados', views.eventosEncerrados, name = 'eventosencerrados'),
]