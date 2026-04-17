from django.db import models
from accounts.models import Usuario

class Profesional(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='profesional'
    )
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr/Dra. {self.usuario.get_full_name()} - {self.especialidad}"

class HorarioDisponible(models.Model):
    DIAS = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
    ]
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    dia_semana = models.IntegerField(choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.profesional} - {self.get_dia_semana_display()} {self.hora_inicio}"

class Turno(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('completado', 'Completado'),
    ]
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='turnos_paciente'
    )
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name='turnos_profesional'
    )
    fecha_hora = models.DateTimeField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )
    servicio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.paciente} con {self.profesional} - {self.fecha_hora}"