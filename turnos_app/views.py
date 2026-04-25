from django.shortcuts import render
from .models import Turno, Profesional, HorarioDisponible
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.utils import timezone # Para manejar fechas
from django.shortcuts import get_object_or_404, redirect #error 404
from django.contrib.auth.decorators import login_required
from .forms import RegistroPacienteForm
from django.contrib.auth import login, get_user_model
User = get_user_model()

def home(request):
    return HttpResponse("<h1>¡Bienvenido al Sistema de Turnos!</h1><p>El backend ya está unificado.</p>")

#RECEPCIONASITA:
@login_required # Si no está logueado, lo manda al login automáticamente
def panel_recepcion(request):
    # Verificamos que el usuario sea RECEPCIONISTA (según el modelo de Pri)
    if request.user.rol != 'recepcionista':
        return HttpResponseForbidden("No tenés permiso para entrar acá, lince.")

    hoy = timezone.now().date()
    turnos_hoy = Turno.objects.filter(fecha_hora__date=hoy)
    
    return render(request, 'accounts/home_recepcionista.html', {
        'turnos': turnos_hoy
    })

def cancelar_turno(request, turno_id):
    # Buscamos el turno, si no existe tira error 404
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'CAN'
    turno.save()
    # Volvemos a la página de recepción para ver el cambio
    return redirect('panel_recepcion')

def confirmar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'CON' # CON de Confirmado
    turno.save()
    return redirect('panel_recepcion')

#PROFESIONAL:
@login_required
def panel_profesional(request):
    profesional = get_object_or_404(Profesional, user=request.user)
    
    # Turnos que tiene que atender (Confirmados)
    pendientes = Turno.objects.filter(estado='CON') # Luego filtraremos por el ID del médico
    
    # Turnos que ya atendió hoy (Completados)
    atendidos = Turno.objects.filter(estado='COM')
    
    return render(request, 'accounts/home_profesional.html', {
        'turnos': pendientes,
        'atendidos': atendidos
    })

def completar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'COM' # Estado: Completado
    turno.save()
    return redirect('panel_profesional')

@login_required
def gestionar_horarios(request):
    # Solo los profesionales pueden entrar acá
    if request.user.rol != 'profesional':
        return redirect('home_paciente')

    if request.method == 'POST':
        dia = request.POST.get('dia')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')
        
        # Guardamos el nuevo horario vinculado al médico logueado
        HorarioDisponible.objects.create(
            profesional=request.user,
            dia_semana=dia,
            hora_inicio=inicio,
            hora_fin=fin
        )
        return redirect('gestionar_horarios')

    horarios = HorarioDisponible.objects.filter(profesional=request.user).order_by('dia_semana', 'hora_inicio')
    return render(request, 'turnos/gestionar_horarios.html', {'horarios': horarios})

@login_required
def eliminar_horario(request, horario_id):
    # Buscamos el horario que tenga ese ID Y que pertenezca al médico logueado (por seguridad)
    horario = HorarioDisponible.objects.get(id=horario_id, profesional=request.user)
    horario.delete()
    return redirect('gestionar_horarios')

#REGISTRO DE PACIENTES
def registro_paciente(request):
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Lo logueamos automáticamente
            return redirect('home_paciente') # Lo mandamos a su panel
    else:
        form = RegistroPacienteForm()
    
    return render(request, 'accounts/registro.html', {'form': form})

@login_required
def home_paciente(request):
    # Ya tenemos el objeto 'user' disponible por defecto en el template
    # pero podemos pasar datos extra si quisiéramos.
    return render(request, 'accounts/home_paciente.html')

@login_required
def redirect_by_role(request):
    # Verificamos el rol del usuario logueado
    if request.user.rol == 'admin':
        return redirect('/admin/')
    elif request.user.rol == 'profesional':
        return redirect('panel_profesional')
    elif request.user.rol == 'recepcionista':
        return redirect('panel_recepcion')
    else:
        # Por defecto, si es paciente o no tiene rol, va a su home
        return redirect('home_paciente')
    
@login_required
def seleccion_profesional(request): 
    # Traemos a todos los usuarios que tengan el rol de profesional
    profesionales = User.objects.filter(rol='profesional') 
    return render(request, 'turnos/seleccion_profesional.html', {'profesionales': profesionales}) #Lista de medicos que el paciente puede elegir

@login_required
def disponibilidad_medico(request, profesional_id):
    medico = User.objects.get(id=profesional_id)
    horarios = HorarioDisponible.objects.filter(profesional=medico).order_by('dia_semana', 'hora_inicio')
    
    return render(request, 'turnos/disponibilidad_medico.html', {
        'medico': medico,
        'horarios': horarios
    }) #Muestra horarios disponibles