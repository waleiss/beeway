from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from administrador.models import Event
from administrador.forms import EventForm
from .forms import AdquirirVoucherForm
from .models import Voucher


def checagem_grupousuario(user):
    """ se for usuario administrador, redireciona para a pagina de login. """ 
    group = Group.objects.get(name='Usuario')
    return group in user.groups.all()

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def Home(request):
    eventos = Event.objects.order_by('data_e_hora')[:6]
    return (render(request, 'usuario/home.html', {'eventos': eventos}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def todosEventos(request):
    search = request.GET.get('search')
    if search:
        eventos_lista = Event.objects.filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.all().order_by('data_e_hora')
        
        """ Adicionar isso quando a paginação puder aparecer na tela
        paginator = Paginator(eventos_lista, 12)
        page = request.GET.get('page')
        eventos = paginator.get_page(page) """
    
    return (render(request, 'usuario/todos.eventos.html', {'eventos': eventos_lista}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def Sobre(request):
    return (render(request, 'usuario/sobre.html'))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def descEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    return (render(request, 'usuario/desc_evento.html', {'evento' : evento}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def verVoucher(request, id):
    voucher = get_object_or_404(Voucher,pk=id)
    evento = voucher.evento
    usuario = voucher.usuario
    return (render(request, 'usuario/voucher.html', {'voucher' : voucher, 'evento' : evento, 'usuario' : usuario}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def adquirirVoucher(request, id):
    evento = get_object_or_404(Event, pk=id)

    if request.method == 'POST':
        # Criar uma instância do form com os dados submetidos
        form = AdquirirVoucherForm(request.POST)

        # Verificar se os dados são válidos
        if form.is_valid():
            #verifica se o numero de ingressos já não acabou
            if evento.voucher_set.count() >= evento.max_ingressos:
                messages.error(request, f'Acabaram os vouchers para o evento "{ evento.titulo }" ', extra_tags='esgotado_voucher')
                return redirect('/usuario/todos.eventos')
            else:
                voucher = Voucher.objects.create(usuario=request.user, evento=evento,)
                messages.success(request, f'Voucher para o evento {evento.titulo} adquirido com sucesso!', extra_tags='conseguiu_voucher')
                return HttpResponseRedirect(reverse('usuariover_voucher', args=[voucher.id]))

    else:
        # Criar uma instância do form vazio
        form = AdquirirVoucherForm()

    return (render(request, 'usuario/adquirir_voucher.html', {'form': form, 'evento': evento}))