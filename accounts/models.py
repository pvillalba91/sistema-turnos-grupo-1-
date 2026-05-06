from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('paciente', 'Paciente'),
        ('profesional', 'Profesional'),
        ('recepcionista', 'Recepcionista'),
        ('admin', 'Administrador'),
    ]
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='paciente'
    )
    telefono = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"{self.username} ({self.rol})"