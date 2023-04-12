from django.db import models

class Event(models.Model):
    
    titulo = models.CharField(max_length=50)
    local = models.CharField(max_length=150)
    data_e_hora_inicio = models.DateTimeField()
    data_e_hora_termino = models.DateTimeField()
    descricao = models.TextField()
    def __str__(self):
        return self.titulo