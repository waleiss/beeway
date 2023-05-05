from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AdquirirVoucherForm, EventForm, CadastroForm
from .models import Voucher, Event

#Usuario

@login_required
def Home(request):
    eventos = Event.objects.order_by('-criado_em')[:6]
    agora = timezone.now()
    return (render(request, 'home.html', {'eventos': eventos, 'agora': agora}))

@login_required
def todosEventos(request):
    agora = timezone.now()
    search = request.GET.get('search')
    if search:
        eventos_lista = Event.objects.filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.all().order_by('-criado_em')
    
    return (render(request, 'todos.eventos.html', {'eventos': eventos_lista, 'agora': agora}))

@login_required
def Sobre(request):
    return (render(request, 'sobre.html'))

@login_required
def descEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    agora = timezone.now()
    return (render(request, 'desc_evento.html', {'evento' : evento, 'agora' : agora}))

@login_required
def verVoucher(request, id):
    voucher = get_object_or_404(Voucher,pk=id)
    evento = voucher.evento
    usuario = voucher.usuario
    if usuario != request.user:
        messages.error(request, 'Você não possui acesso a esse voucher', extra_tags='esgotado_voucher')
        return redirect('/usuario/todos.eventos')
    else:
        return (render(request, 'voucher.html', {'voucher' : voucher, 'evento' : evento, 'usuario' : usuario}))

@login_required
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
                return redirect('todos.eventos')
            elif evento.data_e_hora < agora:
                messages.error(request, f'O evento "{ evento.titulo }" já ocorreu ', extra_tags='esgotado_voucher')
                return redirect('todos.eventos')
            else:
                voucher = Voucher.objects.create(usuario=request.user, evento=evento,)
                messages.success(request, f'Voucher para o evento {evento.titulo} adquirido com sucesso!', extra_tags='conseguiu_voucher')
                return HttpResponseRedirect(reverse('ver_voucher', args=[voucher.id]))

    else:
        # Criar uma instância do form vazio
        form = AdquirirVoucherForm()

    return (render(request, 'adquirir_voucher.html', {'form': form, 'evento': evento}))

#Admin

def Raiz (request):
    return redirect('/home')

def Cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuário "{username}" cadastrado com sucesso!', extra_tags='cadastrou')
            return redirect('login')
    else:
        form = CadastroForm()
    return (render(request, 'registration/cadastro.html', {'form':form}))

def rSenha(request):
    return (render(request, 'registration/rSenha.html'))

@login_required
def meusEventos(request):
    search = request.GET.get('search')
    
    if search:
        eventos_lista = Event.objects.filter(usuario=request.user).filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.filter(usuario=request.user).order_by('-criado_em')
    
    return (render(request, 'meus.eventos.html', {'eventos': eventos_lista}))

@login_required
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
                usuario=request.user
            )
            # Salva o novo evento no banco de dados
            novo_evento.save()
            messages.success(request, f'Evento "{novo_evento.titulo}" adicionado com sucesso!', extra_tags='adicionou_evento')
            return redirect('/todos.eventos')
    else:
        form = EventForm()
    return(render(request, 'addevento.html', {'form':form}))

@login_required
def editarEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    if evento.usuario != request.user:
        return redirect('/home')
    else:
        if (request.method == 'POST'):
            form = EventForm(request.POST, instance=evento)
            if form.is_valid():
                form.save()
                messages.success(request, f'Evento "{evento.titulo}" editado com sucesso!', extra_tags='operou_evento')
                return redirect('/meus.eventos')
            else:
                return(render(request, 'editevento.html', {'form':form, 'evento':evento}))
        else:
            form = EventForm(instance=evento)
        return(render(request, 'editevento.html', {'form':form, 'evento':evento}))

@login_required
def deletarEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    if evento.usuario != request.user:
        return redirect('/home')
    else:
        evento.delete()
        messages.success(request, f'Evento "{evento.titulo}" deletado com sucesso!', extra_tags='operou_evento')
        return redirect('/meus.eventos')
    