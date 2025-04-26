from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CrearEmpleadoForm

@login_required
def crear_empleado(request):
    if request.user.rol != 4:  # Solo rol administrador
        return redirect('index')  # o una página de acceso denegado

    if request.method == 'POST':
        form = CrearEmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # o donde quieras
    else:
        form = CrearEmpleadoForm()

    return render(request, 'crear_empleado/crear_empleado.html', {'form': form})
