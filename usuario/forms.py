from django import forms
from django.contrib.auth.models import User
from administrador.models import Event
from .models import Voucher
from django.core.exceptions import ValidationError
from .creditcard_fields import CreditCardField, ExpiryDateField, VerificationValueField


class AdquirirVoucherForm(forms.Form):
    nome_titular = forms.CharField(max_length=100)
    numero_cartao = CreditCardField(required=True)
    data_validade = ExpiryDateField(required=True)
    cvv = VerificationValueField(required=True)