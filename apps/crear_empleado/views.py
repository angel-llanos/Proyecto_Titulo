from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CrearEmpleadoForm

@login_required
def crear_empleado(request):
    if request.user.rol != 4: #solo rol admin
        return redirect('index')

    if request.method == 'POST':
        form = CrearEmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CrearEmpleadoForm()

    return render(request, 'crear_empleado/crear_empleado.html', {'form': form})
