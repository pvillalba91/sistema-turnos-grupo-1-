from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegistroPacienteForm(UserCreationForm):
    # Definimos los campos con etiquetas claras
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Email")
    telefono = forms.CharField(
        required=True, 
        label="Teléfono (WhatsApp)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1122334455'}))
    
    # El campo DNI con el truco para el teclado numérico del celu
    dni = forms.CharField(
        label="DNI", 
        widget=forms.TextInput(attrs={
            'type': 'number',        # Fuerza teclado numérico
            'inputmode': 'numeric',  # Refuerza la instrucción para móviles
            'pattern': '[0-9]*'      # Asegura solo números
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Quitamos 'username' y agregamos los nuevos
        fields = ('dni', 'first_name', 'last_name', 'email', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Agregamos la clase de Bootstrap a cada input
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            # Limpiamos los textos de ayuda
            self.fields[field].help_text = None
            
        # CAMBIO DE ETIQUETAS ESPECÍFICO:
        if 'password1' in self.fields:
            self.fields['password1'].label = "Contraseña"
        if 'password2' in self.fields:
            self.fields['password2'].label = "Repetir contraseña"

    def save(self, commit=True):
        user = super().save(commit=False)
        # El username de Django es obligatorio internamente, 
        # así que usamos el DNI como nombre de usuario.
        user.username = self.cleaned_data['dni'] 
        user.rol = 'paciente'
        if commit:
            user.save()
        return user
    
