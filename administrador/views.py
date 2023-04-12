from django.shortcuts import render, get_object_or_404
from .models import Event

def Login (request):
    return (render(request, 'pages/login.html'))

def Cadastro(request):
    return (render(request, 'pages/cadastro.html'))

def rSenha(request):
    return (render(request, 'pages/rSenha.html'))

def Home(request):
    return (render(request, 'pages/home.html'))

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
    