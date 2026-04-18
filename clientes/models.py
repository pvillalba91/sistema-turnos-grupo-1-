from django.db import models
from accounts.models import Usuario

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10)
    fecha_nac = models.DateField()

    def __str__(self):
        return f"Cliente: {self.usuario.nombre}"