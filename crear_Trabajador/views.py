from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CrearTrabajadorForm

@login_required
def crear_trabajador(request):
    if request.user.rol != 4:  # Solo rol administrador
        return redirect('index')  # o una página de acceso denegado

    if request.method == 'POST':
        form = CrearTrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # o donde quieras
    else:
        form = CrearTrabajadorForm()

    return render(request, 'crear_trabajador/crear_trabajador.html', {'form': form})
