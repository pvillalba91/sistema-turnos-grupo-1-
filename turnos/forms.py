from django import forms
from .models import Turno, Profesional
from django.utils import timezone

class ReservaTurnoForm(forms.Form):
    especialidad = forms.ChoiceField(
        label='Especialidad',
        choices=[]
    )
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.none(),
        label='Médico disponible',
        empty_label='Seleccioná un médico'
    )
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    servicio = forms.CharField(
        label='Motivo de consulta (opcional)',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        especialidades = Profesional.objects.values_list(
            'especialidad', 'especialidad'
        ).distinct()
        self.fields['especialidad'].choices = [('', 'Seleccioná una especialidad')] + list(especialidades)
        self.fields['profesional'].queryset = Profesional.objects.all()