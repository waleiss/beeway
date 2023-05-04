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

from django.contrib import admin
from django.urls import path, include
from usuario import views
from django.urls import re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/cadastro', views.Cadastro, name = 'cadastro'),
    path('accounts/rSenha', views.rSenha, name = 'rSenha'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.Raiz, name='raiz'),
    path('', include('usuario.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/beeway/static/favicon.ico')),
]
