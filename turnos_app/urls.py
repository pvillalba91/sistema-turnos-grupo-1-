from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recepcion/', views.panel_recepcion, name='panel_recepcion'),
    #ruta para cancelar:
    path('recepcion/cancelar/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path('recepcion/confirmar/<int:turno_id>/', views.confirmar_turno, name='confirmar_turno'),
    path('profesional/', views.panel_profesional, name='panel_profesional'),
    path('profesional/completar/<int:turno_id>/', views.completar_turno, name='completar_turno'),
    path('registro/', views.registro_paciente, name='registro_nuevo'),
    path('verificar-rol/', views.redirect_by_role, name='redirect_by_role'),
    path('gestionar-horarios/', views.gestionar_horarios, name='gestionar_horarios'),
    path('eliminar-horario/<int:horario_id>/', views.eliminar_horario, name='eliminar_horario'),
    path('reservar/', views.seleccion_profesional, name='seleccion_profesional'),
    path('disponibilidad/<int:profesional_id>/', views.disponibilidad_medico, name='disponibilidad_medico'),
    path('reservar/confirmar-seleccion/', views.confirmar_seleccion_paciente, name='confirmar_seleccion'),
    path('mi-ficha-personal/', views.ver_perfil, name='ver_perfil_fijo'),
    path('mis-turnos/', views.mis_turnos, name='mis_turnos'),

]