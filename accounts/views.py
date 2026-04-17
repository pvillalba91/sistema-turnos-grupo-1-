from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_paciente')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'paciente':
                return redirect('home_paciente')
            elif user.rol == 'profesional':
                return redirect('home_profesional')
            elif user.rol == 'recepcionista':
                return redirect('home_recepcionista')
            elif user.rol == 'admin':
                return redirect('home_admin')
            else:
                return redirect('home_admin')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_paciente(request):
    return render(request, 'accounts/home_paciente.html')

@login_required
def home_profesional(request):
    return render(request, 'accounts/home_profesional.html')

@login_required
def home_recepcionista(request):
    return render(request, 'accounts/home_recepcionista.html')

@login_required
def home_admin(request):
    return render(request, 'accounts/home_admin.html')