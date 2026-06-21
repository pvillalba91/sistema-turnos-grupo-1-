from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Teléfono (WhatsApp)'
    )
    rol = forms.ChoiceField(
        choices=Usuario.ROL_CHOICES,
        label='Tipo de cuenta'
    )

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'rol',
            'password1',
            'password2'
        ]