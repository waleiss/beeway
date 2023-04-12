from django.db import models

class Event(models.Model):
    
    nomeevento = models.CharField(max_length=50)
    local = models.CharField(max_length=50)
    datahora_inicio = models.DateTimeField()
    datahora_termino = models.DateTimeField()
    descricao = models.TextField()