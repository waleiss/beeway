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
    def __str__(self):
        return self.titulo
