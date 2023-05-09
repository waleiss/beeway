from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, F, Count, Value
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import AdquirirVoucherForm, EventForm, CadastroForm
from .models import Voucher, Event

#Usuario
@login_required
def Perfil(request):
    usuario = request.user
    return (render(request, 'perfil.html', {'usuario': usuario}))

@login_required
def Home(request):
    agora = timezone.now()
    #Não aparece os eventos que ja passaram do tempo e nem os esgotados
    eventos = Event.objects.annotate(num_vouchers=Count('voucher')).filter(Q(data_e_hora__gte=agora) & Q(num_vouchers__lt=F('max_ingressos') )).order_by('-criado_em')[:6]
    usuario = request.user
    return (render(request, 'home.html', {'eventos': eventos, 'agora': agora, 'usuario': usuario}))

@login_required
def todosEventos(request):
    agora = timezone.now()
    #Não aparece os eventos que ja passaram do tempo e nem os esgotados
    search = request.GET.get('search')
    if search:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(Q(data_e_hora__gte=agora) & Q(num_vouchers__lt=F('max_ingressos'))).filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(Q(data_e_hora__gte=agora) & Q(num_vouchers__lt=F('max_ingressos') )).order_by('-criado_em')
    
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
    if (usuario == request.user or evento.usuario == request.user):
        return (render(request, 'voucher.html', {'voucher' : voucher, 'evento' : evento, 'usuario' : usuario}))
    else:
        messages.error(request, 'Você não possui acesso a esse voucher', extra_tags='esgotado_voucher')
        return redirect('/todos.eventos')
       

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
                return redirect('/todos.eventos')
            elif evento.data_e_hora < agora:
                messages.error(request, f'O evento "{ evento.titulo }" já ocorreu ', extra_tags='esgotado_voucher')
                return redirect('/todos.eventos')
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

def meusVouchers(request):
    search = request.GET.get('search')

    if search:
        vouchers_lista = Voucher.objects.filter(usuario=request.user).filter(evento__titulo__icontains=search)
    else:
        vouchers_lista = Voucher.objects.filter(usuario=request.user).order_by('-criado_em')

    return (render(request, 'meus.vouchers.html', {'vouchers': vouchers_lista}))

@login_required
def eventosEncerrados(request):
    agora = timezone.now()
    search = request.GET.get('search')
# Count conta o numero de vouchers do evento, depois Q coloca um OU no filtro, e ao mesmo tempo F comparar o numero de vouchers com o max de ingressos
    if search:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(Q(data_e_hora__lt=agora) | Q(num_vouchers__gte=F('max_ingressos'))).filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(Q(data_e_hora__lt=agora) | Q(num_vouchers__gte=F('max_ingressos'))).order_by('-criado_em')
    
    return (render(request, 'eventos.encerrados.html', {'eventos': eventos_lista, 'agora': agora}))

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

@login_required
def meusEventosComprados(request):
    search = request.GET.get('search')
    
    if search:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(usuario=request.user).filter(num_vouchers__gt=0).filter(titulo__icontains=search)
    else:
        eventos_lista = Event.objects.annotate(num_vouchers=Count('voucher')).filter(usuario=request.user).filter(num_vouchers__gt=0).order_by('-criado_em')
    
    return (render(request, 'eventos_comprados.html', {'eventos': eventos_lista}))

@login_required
def listaCompradores(request, id):
    search = request.GET.get('search')
    evento = get_object_or_404(Event, pk=id)
    if evento.usuario != request.user:
        return redirect('/home')
    else:
        if search:
             vouchers_lista = Voucher.objects.filter(Q(evento=id) & (Q(usuario__first_name__icontains=search) | Q(usuario__last_name__icontains=search)))
        else:
            vouchers_lista = Voucher.objects.filter(evento=id).order_by('criado_em')
    
        return (render(request, 'lista_compradores.html', {'vouchers': vouchers_lista, 'evento': evento}))

@login_required
def checkVoucher(request, id):
    voucher = get_object_or_404(Voucher, pk=id)
    if voucher.evento.usuario != request.user:
        return redirect('/home')
    else:
        voucher.check_in = '2'
        voucher.save()
        messages.success(request, f'Voucher de "{voucher.usuario.first_name}" checado com sucesso!', extra_tags='operou_voucher')
        
        url_referencia = request.META.get('HTTP_REFERER')
        return redirect(url_referencia)

@login_required
def uncheckVoucher(request, id):
    voucher = get_object_or_404(Voucher, pk=id)
    if voucher.evento.usuario != request.user:
        return redirect('/home')
    else:    
        voucher.check_in = '1'
        voucher.save()
        messages.success(request, f'Voucher de "{voucher.usuario.first_name}" deschecado com sucesso!', extra_tags='operou_voucher')
        
        url_referencia = request.META.get('HTTP_REFERER')
        return redirect(url_referencia)

