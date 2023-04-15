from django.urls import path
from . import views

urlpatterns = [
    path('usuario/home', views.Home, name = 'usuariohome'),


]