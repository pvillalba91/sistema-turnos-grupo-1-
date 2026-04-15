from django.db import models
from django.contrib.auth.models import User

class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.especialidad}"

class Turno(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('CON', 'Confirmado'),
        ('CAN', 'Cancelado'),
        ('COM', 'Completado'),
    ]
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    # Aquí Gianluca luego agregará las relaciones con Cliente y Profesional