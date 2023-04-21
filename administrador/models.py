from django.db import models
from django.contrib.auth.models import User
import random, string

class Event(models.Model):
    
    titulo = models.CharField(max_length=50)
    local = models.CharField(max_length=150)
    data_e_hora = models.DateTimeField()
    descricao = models.TextField()
    contato = models.CharField(max_length=150)
    max_ingressos = models.PositiveSmallIntegerField()
    preco = models.DecimalField(decimal_places=2, max_digits=10)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

User._meta.get_field('email')._unique = True