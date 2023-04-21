from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['titulo', 'local', 'data_e_hora', 'descricao', 'contato', 'max_ingressos', 'preco']
        widgets = {
            'data_e_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'preco': forms.NumberInput(attrs={'type': 'number', 'step': '0.01'})
        }

class CadastroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Necessário.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Necessário.')
    email = forms.EmailField(max_length=254, required=True, help_text='Necessário. Escreva um endereço de email válido.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )