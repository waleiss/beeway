from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['titulo', 'local', 'data_e_hora', 'descricao']
        widgets = {
            'data_e_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }