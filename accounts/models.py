from django.db import models

ROL_CHOICES = [
    ('cliente', 'Cliente'),
    ('profesional', 'Profesional'),
    ('recepcionista', 'Recepcionista'),
    ('admin', 'Administrador'),
]

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"