from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.reservar_turno, name='reservar_turno'),
    path('confirmacion/<int:turno_id>/', views.confirmacion_turno, name='confirmacion_turno'),
    path('mis-turnos/', views.mis_turnos, name='mis_turnos'),
]