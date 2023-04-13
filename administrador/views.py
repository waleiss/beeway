from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event

#Fazer com que todas as paginas de administrador necessitem que o user esteja logado e seja administrador
def checagem_permissao(user):
    return user.groups.filter(name='administrador').exists()
    
def Login (request):
    return (render(request, 'pages/login.html'))

def Cadastro(request):
    return (render(request, 'pages/cadastro.html'))

def rSenha(request):
    return (render(request, 'pages/rSenha.html'))

@login_required
@user_passes_test(checagem_permissao, login_url='/login/')
def Home(request):
    eventos = Event.objects.order_by('-data_e_hora_inicio')[:6]
    return (render(request, 'pages/home.html', {'eventos': eventos}))

def todosEventos(request):
    eventos = Event.objects.all().order_by('-data_e_hora_inicio')
    return (render(request, 'pages/todos.eventos.html', {'eventos': eventos}))

def Sobre(request):
    return (render(request, 'pages/sobre.html'))

def descEvento(request, id):
    evento = get_object_or_404(Event, pk=id)
    return (render(request, 'pages/desc_evento.html', {'evento' : evento}))

def Voucher(request):
    return (render(request, 'pages/voucher.html'))

def adicionarEvento(request):
    return(render(request, ))
    