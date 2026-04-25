from django.db import models
from accounts.models import Usuario

class Perfil(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    dni = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    obra_social = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name()}"