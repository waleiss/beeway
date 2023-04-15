from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from administrador.models import Event
from administrador.forms import EventForm

# Create your views here.
def checagem_grupousuario(user):
    """ se for usuario administrador, redireciona para a pagina de login. """ 
    group = Group.objects.get(name='Usuario')
    return group in user.groups.all()

@user_passes_test(checagem_grupousuario, login_url = '/accounts/login', redirect_field_name='')
def Home(request):
    eventos = Event.objects.order_by('data_e_hora')[:6]
    return (render(request, 'pages/homeUsuario.html', {'eventos': eventos}))
