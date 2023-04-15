"""beeway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
""" As views de cadastro, raiz e verificação se o usuario é admin ou usuario está no app de administrador"""
from django.contrib import admin
from django.urls import path, include
from administrador import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro', views.Cadastro, name = 'cadastro'),
    path('rSenha', views.rSenha, name = 'rSenha'),
    path('', include('administrador.urls')),
    path('accounts/cadastro', views.Cadastro, name = 'cadastro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('usuario.urls')),
    path('', views.Raiz, name='raiz'),
    path('verificador', views.Verificador, name='verificador'),
]
