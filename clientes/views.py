from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil
from .forms import PerfilForm, UsuarioForm

@login_required
def ver_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'clientes/perfil.html', {'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, instance=perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('ver_perfil')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)
    return render(request, 'clientes/editar_perfil.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form
    })