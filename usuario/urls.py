from django.urls import path
from . import views

urlpatterns = [
    path('home', views.Home, name = 'home'),
    path('meus.vouchers', views.meusVouchers, name = 'meusvouchers'),
    path('meus.eventos', views.meusEventos, name = 'meuseventos'),
    path('meus.eventos/eventos_comprados', views.meusEventosComprados, name = 'meuseventoscomprados'),
    path('meus.eventos/lista_compradores/<int:id>', views.listaCompradores, name = 'listacompradores'),
    path('meus.eventos/check_voucher/<int:id>', views.checkVoucher, name = 'checkvoucher'),
    path('meus.eventos/uncheck_voucher/<int:id>', views.uncheckVoucher, name = 'uncheckvoucher'),
    path('editar_evento/<int:id>', views.editarEvento, name = 'editar_evento'),
    path('deletar_evento/<int:id>', views.deletarEvento, name = 'deletar_evento'),
    path('eventos.encerrados', views.eventosEncerrados, name = 'eventosencerrados'),
    path('perfil', views.Perfil, name = 'meuperfil'),
    path('todos.eventos', views.todosEventos, name = 'todoseventos'),
    path('adicionar_evento', views.adicionarEvento, name = 'adicionar_evento'),
    path('desc_evento/<int:id>', views.descEvento, name = 'desc_evento'),
    path('adquirir_voucher/<int:id>', views.adquirirVoucher, name = 'adquirir_voucher'),
    path('voucher/<int:id>', views.verVoucher, name = 'ver_voucher'),
    path('sobre', views.Sobre, name = 'sobre'),
]