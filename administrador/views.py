from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event
from .forms import EventForm

#Fazer com que todas as paginas de administrador necessitem que o user esteja logado e seja administrador
def checagem_permissao(user):
    return user.groups.filter(name='administrador').exists()
    
def Login (request):
    return (render(request, 'pages/login.html'))

def Cadastro(request):
    return (render(request, 'pages/cadastro.html'))

def rSenha(request):
    return (render(request, 'pages/rSenha.html'))

def Home(request):
    eventos = Event.objects.order_by('data_e_hora')[:6]
    return (render(request, 'pages/home.html', {'eventos': eventos}))

def todosEventos(request):
    eventos = Event.objects.all().order_by('data_e_hora')
    return (render(request, 'pages/todos.eventos.html', {'eventos': eventos}))

def Sobre(request):
    return (render(request, 'pages/sobre.html'))

def descEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    return (render(request, 'pages/desc_evento.html', {'evento' : evento}))

def Voucher(request):
    return (render(request, 'pages/voucher.html'))

def adicionarEvento(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            novo_evento = Event(
                titulo=form.cleaned_data['titulo'],
                local=form.cleaned_data['local'],
                data_e_hora=form.cleaned_data['data_e_hora'],
                descricao=form.cleaned_data['descricao'],
            )
            # Salva o novo evento no banco de dados
            novo_evento.save()
            return redirect('todos.eventos')
    else:
        form = EventForm()
    return(render(request, 'pages/addevento.html', {'form':form}))

def editarEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    
    if (request.method == 'POST'):
        form = EventForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('/administrador/todos.eventos')
        else:
            return(render(request, 'pages/editevento.html', {'form':form, 'evento':evento}))
    else:
        form = EventForm(instance=evento)
    return(render(request, 'pages/editevento.html', {'form':form, 'evento':evento}))
    