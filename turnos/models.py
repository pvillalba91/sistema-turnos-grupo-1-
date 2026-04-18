from django.db import models
from clientes.models import Cliente
from profesionales.models import Profesional

ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('confirmado', 'Confirmado'),
    ('cancelado', 'Cancelado'),
    ('completado', 'Completado'),
]

class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    servicio = models.CharField(max_length=100)

    def __str__(self):
        return f"Turno {self.id} - {self.cliente} con {self.profesional}"