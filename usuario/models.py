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

class Voucher(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Event, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=13, unique=True)

    @classmethod
    def generate_random_code(cls):
        """Generate a random string of letters and digits."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generate a unique ticket code
            codigo = self.generate_random_code()
            while Voucher.objects.filter(codigo=codigo).exists():
                codigo = self.generate_random_code()
            self.codigo = codigo
        super().save(*args, **kwargs)