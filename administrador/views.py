from django.shortcuts import render

# Create your views here.
def Login (request):
    return (render(request, 'pages/login.html'))
def Cadastro(request):
    return (render(request, 'pages/cadastro.html'))
def rSenha(request):
    return (render(request, 'pages/rSenha.html'))
def Home(request):
    return (render(request, 'pages/home.html'))
def todosEventos(request):
    return (render(request, 'pages/todos.eventos.html'))
def Sobre(request):
    return (render(request, 'pages/sobre.html'))
def descEvento(request):
    return (render(request, 'pages/desc_evento.html'))
def Voucher(request):
    return (render(request, 'pages/voucher.html'))