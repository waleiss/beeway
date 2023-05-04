from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Voucher, Event
from django.core.exceptions import ValidationError
from .creditcard_fields import CreditCardField, ExpiryDateField, VerificationValueField

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

class AdquirirVoucherForm(forms.Form):
    nome_titular = forms.CharField(max_length=100)
    numero_cartao = CreditCardField(required=True)
    data_validade = ExpiryDateField(required=True)
    cvv = VerificationValueField(required=True)