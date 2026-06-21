from django.conf import settings
from django.db import models
from clientes.models import Perfil

class Profesional(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_profesional'
    )
    especialidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.especialidad}"

class HorarioDisponible(models.Model):
    profesional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
        (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_turno = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.get_dia_semana_display()}: {self.hora_inicio} a {self.hora_fin} (cada {self.duracion_turno} min)"

class Turno(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('CON', 'Confirmado'),
        ('CAN', 'Cancelado'),
        ('COM', 'Completado'),
    ]
    cliente = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, null=True, blank=True)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    servicio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Turno {self.id} - {self.cliente} con {self.profesional} el {self.fecha_hora}"


def asignar_turno_automatico(fecha_hora_solicitada, especialidad, cliente_perfil):
    """
    Motor de asignación automática de turnos.
    Busca el primer profesional disponible para la fecha/hora y especialidad solicitadas.
    """
    dia_semana = fecha_hora_solicitada.weekday()
    hora_solicitada = fecha_hora_solicitada.time()

    profesionales = Profesional.objects.filter(especialidad=especialidad)

    for profesional in profesionales:
        horario_disponible = HorarioDisponible.objects.filter(
            profesional=profesional.user,
            dia_semana=dia_semana,
            hora_inicio__lte=hora_solicitada,
            hora_fin__gt=hora_solicitada
        ).exists()

        if not horario_disponible:
            continue

        turno_existente = Turno.objects.filter(
            profesional=profesional,
            fecha_hora=fecha_hora_solicitada,
            estado__in=['PEN', 'CON']
        ).exists()

        if not turno_existente:
            turno = Turno.objects.create(
                cliente=cliente_perfil,
                profesional=profesional,
                fecha_hora=fecha_hora_solicitada,
                estado='CON',
                servicio=especialidad
            )
            return turno

    return None