from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservaTurnoForm
from .models import Turno, Profesional
from django.utils import timezone

@login_required
def reservar_turno(request):
    if request.method == 'POST':
        form = ReservaTurnoForm(request.POST)
        if form.is_valid():
            especialidad = form.cleaned_data['especialidad']
            profesional = form.cleaned_data['profesional']
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            servicio = form.cleaned_data['servicio']
            fecha_hora = timezone.datetime.combine(fecha, hora)
            turno = Turno.objects.create(
                paciente=request.user,
                profesional=profesional,
                fecha_hora=fecha_hora,
                servicio=servicio,
                estado='pendiente'
            )
            messages.success(request, 'Turno reservado correctamente')
            return redirect('confirmacion_turno', turno_id=turno.id)
    else:
        form = ReservaTurnoForm()
    return render(request, 'turnos/reservar_turno.html', {'form': form})

@login_required
def confirmacion_turno(request, turno_id):
    turno = Turno.objects.get(id=turno_id, paciente=request.user)
    return render(request, 'turnos/confirmacion_turno.html', {'turno': turno})

@login_required
def mis_turnos(request):
    turnos = Turno.objects.filter(
        paciente=request.user
    ).order_by('-fecha_hora')
    return render(request, 'turnos/mis_turnos.html', {'turnos': turnos})