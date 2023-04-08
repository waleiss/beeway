from django.shortcuts import render

# Create your views here.
def Login (request):
    return (render(request, 'pages/login.html'))
def Cadastro(request):
    return (render(request, 'pages/cadastro.html'))