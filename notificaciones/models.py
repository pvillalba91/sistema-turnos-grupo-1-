from django.db import models
from turnos.models import Turno

TIPO_CHOICES = [
    ('confirmacion', 'Confirmación'),
    ('recordatorio', 'Recordatorio'),
    ('cancelacion', 'Cancelación'),
]

class Notificacion(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    canal = models.CharField(max_length=20)
    enviado_en = models.DateTimeField(null=True, blank=True)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} - Turno {self.turno.id}"