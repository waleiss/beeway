from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AdquirirVoucherForm, EventForm
from .models import Voucher, Event

#Usuario
def checagem_grupousuario(user):
    """ se for usuario administrador, redireciona para a pagina de login. """ 
    group = Group.objects.get(name='Usuario')
    return group in user.groups.all()

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def Home(request):
    eventos = Event.objects.order_by('-criado_em')[:6]
    return (render(request, 'usuario/home.html', {'eventos': eventos}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def todosEventos(request):
    search = request.GET.get('search')
    if search:
        eventos_lista = Event.objects.filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.all().order_by('-criado_em')
        
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
    agora = timezone.now()
    return (render(request, 'usuario/desc_evento.html', {'evento' : evento, 'agora' : agora}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def verVoucher(request, id):
    voucher = get_object_or_404(Voucher,pk=id)
    evento = voucher.evento
    usuario = voucher.usuario
    if usuario != request.user:
        messages.error(request, 'Você não possui acesso a esse voucher', extra_tags='esgotado_voucher')
        return redirect('/usuario/todos.eventos')
    else:
        return (render(request, 'usuario/voucher.html', {'voucher' : voucher, 'evento' : evento, 'usuario' : usuario}))

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def adquirirVoucher(request, id):
    evento = get_object_or_404(Event, pk=id)
    agora = timezone.now()

    if request.method == 'POST':
        # Criar uma instância do form com os dados submetidos
        form = AdquirirVoucherForm(request.POST)

        # Verificar se os dados são válidos
        if form.is_valid():
            #verifica se o numero de ingressos já não acabou
            if evento.voucher_set.count() >= evento.max_ingressos:
                messages.error(request, f'Acabaram os vouchers para o evento "{ evento.titulo }" ', extra_tags='esgotado_voucher')
                return redirect('/usuario/todos.eventos')
            elif evento.data_e_hora < agora:
                messages.error(request, f'O evento "{ evento.titulo }" já ocorreu ', extra_tags='esgotado_voucher')
                return redirect('/usuario/todos.eventos')
            else:
                voucher = Voucher.objects.create(usuario=request.user, evento=evento,)
                messages.success(request, f'Voucher para o evento {evento.titulo} adquirido com sucesso!', extra_tags='conseguiu_voucher')
                return HttpResponseRedirect(reverse('usuariover_voucher', args=[voucher.id]))

    else:
        # Criar uma instância do form vazio
        form = AdquirirVoucherForm()

    return (render(request, 'usuario/adquirir_voucher.html', {'form': form, 'evento': evento}))

#Admin

@login_required
def Verificador(request):
    if request.user.groups.filter(name='Administrador').exists():
        return redirect('/administrador/home')
    elif request.user.groups.filter(name='Usuario').exists():
        return redirect('/usuario/home')

def Raiz (request):
    return redirect('/administrador/home')

def Cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = Group.objects.get(name='Usuario')
            user.groups.add(grupo)
            return redirect('login')
    else:
        form = CadastroForm()
    return (render(request, 'registration/cadastro.html', {'form':form}))

def rSenha(request):
    return (render(request, 'registration/rSenha.html'))


def adicionarEvento(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            novo_evento = Event(
                titulo=form.cleaned_data['titulo'],
                local=form.cleaned_data['local'],
                data_e_hora=form.cleaned_data['data_e_hora'],
                descricao=form.cleaned_data['descricao'],
                contato=form.cleaned_data['contato'],
                max_ingressos=form.cleaned_data['max_ingressos'],
                preco=form.cleaned_data['preco'],
            )
            # Salva o novo evento no banco de dados
            novo_evento.save()
            messages.success(request, f'Evento "{novo_evento.titulo}" adicionado com sucesso!', extra_tags='operou_evento')
            return redirect('todos.eventos')
    else:
        form = EventForm()
    return(render(request, 'administrador/addevento.html', {'form':form}))

@user_passes_test(checagem_grupoadmin, login_url = '/accounts/login', redirect_field_name='')
def editarEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    
    if (request.method == 'POST'):
        form = EventForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Evento "{evento.titulo}" editado com sucesso!', extra_tags='operou_evento')
            return redirect('/administrador/todos.eventos')
        else:
            return(render(request, 'administrador/editevento.html', {'form':form, 'evento':evento}))
    else:
        form = EventForm(instance=evento)
    return(render(request, 'administrador/editevento.html', {'form':form, 'evento':evento}))

@user_passes_test(checagem_grupoadmin, login_url = '/accounts/login', redirect_field_name='')
def deletarEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    evento.delete()
    messages.success(request, f'Evento "{evento.titulo}" deletado com sucesso!', extra_tags='operou_evento')
    
    return redirect('/administrador/todos.eventos')
    