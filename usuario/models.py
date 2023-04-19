from django.db import models
from django.contrib.auth.models import User
from administrador.models import Event
import random, string

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