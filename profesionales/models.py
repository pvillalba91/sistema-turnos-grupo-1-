from django.db import models
from accounts.models import Usuario

class Profesional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=50)

    def __str__(self):
        return f"Profesional: {self.usuario.nombre}"

class HorarioDisponible(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.profesional.usuario.nombre} - {self.dia_semana}"