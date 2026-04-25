from django import forms
from accounts.models import Usuario
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['dni', 'fecha_nacimiento', 'obra_social', 'direccion']
        labels = {
            'dni': 'DNI',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'obra_social': 'Obra social',
            'direccion': 'Dirección',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'telefono': 'Teléfono (WhatsApp)',
        }