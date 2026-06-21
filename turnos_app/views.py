from django.shortcuts import render
from .models import Turno, Profesional, HorarioDisponible
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.utils import timezone # Para manejar fechas
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404, redirect #error 404
from django.contrib.auth.decorators import login_required
from .forms import RegistroPacienteForm
from django.contrib.auth import login, get_user_model
from datetime import datetime, timedelta
import csv

User = get_user_model()

def home(request):
    return HttpResponse("<h1>¡Bienvenido al Sistema de Turnos!</h1><p>El backend ya está unificado.</p>")

#RECEPCIONASITA:
@login_required
def panel_recepcion(request):
    # 1. Atrapamos la fecha que la recepcionista elige en el calendario
    fecha_str = request.GET.get('fecha')
    ahora = timezone.now()
    
    # 2. Si eligió una fecha, la procesamos. Si no, mostramos el día de hoy.
    if fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_obj = ahora.date()
    else:
        fecha_obj = ahora.date()

    # 3. Filtramos los turnos EXACTAMENTE por ese día
    turnos = Turno.objects.filter(fecha_hora__date=fecha_obj).order_by('fecha_hora')

    # 4. Mandamos todo al HTML
    contexto = {
        'turnos': turnos,
        'fecha_input': fecha_obj.strftime('%Y-%m-%d'), # Esto llena el calendario con la fecha elegida
        'fecha_titulo': fecha_obj # Esto es para poner "Turnos del 25/06/2026"
    }
    
    # OJO: Revisá si el nombre de tu template es este, sino cambialo al que estés usando
    return render(request, 'accounts/home_recepcionista.html', contexto)

def cancelar_turno(request, turno_id):
    # Buscamos el turno, si no existe tira error 404
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'CAN'
    turno.save()
    # En vez de mandar fijo a panel_recepcion:
    if request.user.rol == 'recepcionista':
        return redirect('panel_recepcion')
    return redirect('mis_turnos')

def confirmar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'CON' # CON de Confirmado
    turno.save()
    return redirect('panel_recepcion')

#PROFESIONAL:
@login_required
def panel_profesional(request):
    profesional = get_object_or_404(Profesional, user=request.user)
    
    # 1. Atrapamos la fecha que el médico elige en el calendario
    fecha_str = request.GET.get('fecha')
    ahora = timezone.now()
    
    # 2. Si eligió una fecha, la procesamos. Si no, mostramos el día de hoy.
    if fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_obj = ahora.date()
    else:
        fecha_obj = ahora.date()

    # 3. Filtramos los turnos EXACTAMENTE por ese día y por el profesional logueado
    pendientes = Turno.objects.filter(
        estado='CON', 
        profesional=profesional,
        fecha_hora__date=fecha_obj
    ).order_by('fecha_hora')
    
    atendidos = Turno.objects.filter(
        estado='COM', 
        profesional=profesional,
        fecha_hora__date=fecha_obj
    ).order_by('fecha_hora')
    
    # 4. Mandamos todo al HTML
    contexto = {
        'turnos': pendientes,
        'atendidos': atendidos,
        'fecha_input': fecha_obj.strftime('%Y-%m-%d'),
        'fecha_titulo': fecha_obj
    }
    
    return render(request, 'accounts/home_profesional.html', contexto)

def completar_turno(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'COM' # Estado: Completado
    turno.save()
    return redirect('panel_profesional')

@login_required
def gestionar_horarios(request):
    if request.user.rol != 'profesional':
        return redirect('home_paciente')

    if request.method == 'POST':
        dia = request.POST.get('dia')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')
        duracion = request.POST.get('duracion', 30) # Tomamos la duración del formulario
        
        HorarioDisponible.objects.create(
            profesional=request.user,
            dia_semana=dia,
            hora_inicio=inicio,
            hora_fin=fin,
            duracion_turno=duracion # <-- Agregamos esto
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

@login_required
def exportar_historial_csv(request):
    # Le decimos al navegador que esto va a ser un archivo descargable
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historial_atenciones.csv"'

    # Empezamos a escribir el archivo
    writer = csv.writer(response)
    
    # Fila 1: Los títulos de las columnas
    writer.writerow(['Fecha', 'Hora', 'Paciente', 'DNI', 'Especialidad'])

    # Buscamos al profesional y sus turnos COMPLETADOS
    profesional = get_object_or_404(Profesional, user=request.user)
    atendidos = Turno.objects.filter(profesional=profesional, estado='COM').order_by('-fecha_hora')

    # Recorremos los turnos y llenamos las filas con los datos (usando username como DNI)
    for turno in atendidos:
        writer.writerow([
            turno.fecha_hora.strftime("%d/%m/%Y"),
            turno.fecha_hora.strftime("%H:%M"),
            f"{turno.cliente.usuario.first_name} {turno.cliente.usuario.last_name}",
            turno.cliente.usuario.username,
            turno.servicio
        ])

    return response


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
        # ACÁ EL CAMBIO: Forzamos la ruta exacta para evitar fantasmas
        return redirect('/profesional/') 
    elif request.user.rol == 'recepcionista':
        # ACÁ EL CAMBIO: Forzamos la ruta exacta
        return redirect('/recepcion/') 
    else:
        # Por defecto, si es paciente o no tiene rol, va a su home
        return redirect('home_paciente')
    
@login_required
def seleccion_profesional(request): 
    # En vez de traer Users, traemos los Profesionales con sus datos de usuario vinculados
    profesionales = Profesional.objects.select_related('user').all() 
    return render(request, 'turnos/seleccion_profesional.html', {'profesionales': profesionales})


@login_required
def disponibilidad_medico(request, profesional_id):
    medico = User.objects.get(id=profesional_id)
    # Traemos todos los horarios configurados del médico
    horarios_queryset = HorarioDisponible.objects.filter(profesional=medico)
    
    semana_offset = int(request.GET.get('semana', 0))
    ahora = localtime(timezone.now())
    hoy = ahora.date()
    
    lunes_semana_actual = hoy - timedelta(days=hoy.weekday())
    lunes_objetivo = lunes_semana_actual + timedelta(weeks=semana_offset)
    
    agenda_final = []
    nombres_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    for i in range(7):
        fecha_dia = lunes_objetivo + timedelta(days=i)
        
        bloques_del_dia = horarios_queryset.filter(dia_semana=i)
        turnos_totales_dia = []
        
        # 1. Buscamos TODOS los turnos que ya están ocupados para este médico en esta fecha
        # (Excluimos los cancelados, porque si se canceló, el lugar vuelve a estar libre)
        turnos_ocupados = Turno.objects.filter(
            profesional__user=medico, 
            fecha_hora__date=fecha_dia
        ).exclude(estado='CAN').values_list('fecha_hora__time', flat=True)

        for horario_config in bloques_del_dia:
            inicio_dt = datetime.combine(fecha_dia, horario_config.hora_inicio)
            fin_dt = datetime.combine(fecha_dia, horario_config.hora_fin)
            actual = inicio_dt
            
            while actual + timedelta(minutes=horario_config.duracion_turno) <= fin_dt:
                hora_actual_time = actual.time()
                hora_inicio_str = actual.strftime("%H:%M")
                
                # 2. Verificamos si ya pasó el tiempo
                pasado = (fecha_dia < hoy) or (fecha_dia == hoy and hora_actual_time < ahora.time())
                
                # 3. Verificamos si ya está reservado en la base de datos
                ya_reservado = hora_actual_time in turnos_ocupados
                     
            turnos_totales_dia.append({
                'inicio': hora_inicio_str,
                'ocupado': pasado or ya_reservado,
                'horario_id': horario_config.id
            })
            actual += timedelta(minutes=horario_config.duracion_turno)

        turnos_totales_dia = sorted(turnos_totales_dia, key=lambda x: x['inicio'])

        agenda_final.append({
            'dia_nombre': nombres_dias[i],
            'fecha_txt': fecha_dia.strftime("%d/%m/%Y"),
            'fecha_sql': fecha_dia.strftime("%Y-%m-%d"),
            'turnos': turnos_totales_dia,
            'atiende': bloques_del_dia.exists()
        })

    return render(request, 'turnos/disponibilidad_medico.html', {
        'medico': medico,
        'agenda': agenda_final,
        'semana': semana_offset,
        'prox': semana_offset + 1,
        'prev': semana_offset - 1,
    })

    return render(request, 'turnos/disponibilidad_medico.html', {
        'medico': medico,
        'agenda': agenda_final,
        'semana': semana_offset,
        'prox': semana_offset + 1,
        'prev': semana_offset - 1,
    })

#FORMULARIO DE RESERVA DE TURNO
@login_required
def formulario_reserva(request, medico_id, horario_id):
    medico = User.objects.get(id=medico_id)
    horario = HorarioDisponible.objects.get(id=horario_id)
    
    # Lista de días para validar (0=Lunes, etc.)
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    nombre_dia = dias[horario.dia_semana]

    return render(request, 'turnos/formulario_reserva.html', {
        'medico': medico,
        'horario': horario,
        'nombre_dia': nombre_dia
    })


#CONFIRMACION DE TURNO:
@login_required
def confirmar_seleccion_paciente(request):
    medico_id = request.GET.get('medico')
    inicio = request.GET.get('inicio')
    fecha = request.GET.get('fecha')

    medico = User.objects.get(id=medico_id)

    if request.method == 'POST':
        medico_id_post = request.GET.get('medico')
        inicio_post = request.GET.get('inicio')
        fecha_post = request.GET.get('fecha')

        medico_post = User.objects.get(id=medico_id_post)
        profesional = Profesional.objects.get(user=medico_post)

        fecha_hora_str = f"{fecha_post} {inicio_post}"
        fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        fecha_hora = timezone.make_aware(fecha_hora)

        from clientes.models import Perfil
        perfil, created = Perfil.objects.get_or_create(
            usuario=request.user,
            defaults={'dni': request.user.username}
        )

        Turno.objects.create(
            cliente=perfil,
            profesional=profesional,
            fecha_hora=fecha_hora,
            estado='CON',
            servicio=profesional.especialidad
        )

        return redirect('mis_turnos')

    return render(request, 'turnos/confirmar_turno.html', {
        'medico': medico,
        'inicio': inicio,
        'fecha': fecha,
    })

#VER MI PERFIL (PACIENTE)
@login_required
@login_required
def ver_perfil(request):
    return render(request, 'clientes/perfil.html', {'usuario': request.user})

#MIS TURNOS (PACIENTE)
@login_required
def mis_turnos(request):
    from clientes.models import Perfil
    try:
        perfil = Perfil.objects.get(usuario=request.user)
        turnos = Turno.objects.filter(cliente=perfil).order_by('-fecha_hora')
    except Perfil.DoesNotExist:
        turnos = []
    return render(request, 'turnos/mis_turnos.html', {'turnos': turnos})

#EDITAR PERFIL (PACIENTE)
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.telefono = request.POST.get('telefono', '')
        request.user.save()
        return redirect('ver_perfil_fijo')
    return redirect('ver_perfil_fijo')

#CANCELAR TURNO (PACIENTE)
@login_required
def cancelar_turno_paciente(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'CAN'
    turno.save()
    return redirect('mis_turnos')
