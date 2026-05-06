from django.conf import settings
from django.db import models

class Profesional(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil_profesional'
    )
    especialidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

    def __str__(self):
        # Usamos el email o el nombre de usuario por si no completaron el nombre completo
        return f"{self.user.username} - {self.especialidad}"

class HorarioDisponible(models.Model):
    # En lugar de 'User', usamos 'settings.AUTH_USER_MODEL'
    # Es la forma más segura de referenciar al usuario en Django
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
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    # Aquí Gianluca luego agregará las relaciones con Cliente y Profesional