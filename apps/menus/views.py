from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from apps.reservas.models import Reserva
from .models import Menu
from .forms import MenuForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def menus(request):
    if request.user.is_authenticated:
        if request.user.rol in [3, 4]:  # Admins y staff ven todo
            lista_menus = Menu.objects.all()
        else:
            lista_menus = Menu.objects.filter(activo=True)
    else:
        # Usuarios anónimos solo ven menús activos
        lista_menus = Menu.objects.filter(activo=True)

    context = {'menus': lista_menus}
    return render(request, 'menus/menus.html', context)

# Vista para agregar un nuevo menú (solo administrador)
@login_required
def agregar_menu(request):
    if request.user.rol not in [4, 3]:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menus')
    else:
        form = MenuForm()
    
    return render(request, 'menus/agregar_menu.html', {'form': form})

@login_required
def modificar_menu(request, menu_id):
    if request.user.rol not in [4, 3]:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menú modificado correctamente.')
            return redirect('menus')  # o usa 'menus:lista_menus' si tienes namespace
    else:
        form = MenuForm(instance=menu)

    context = {
        'form': form,
        'menu': menu
    }
    return render(request, 'menus/modificar_menu.html', context)

@login_required
def eliminar_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    # Verifica si hay reservas vinculadas
    reservas_ligadas = Reserva.objects.filter(menu=menu).exists()

    if reservas_ligadas:
        messages.warning(request, "Este menú está asociado a una o más reservas. Solo puede ser desactivado.")
        return redirect('menus')  # o el nombre de tu vista principal

    # Si no hay reservas, eliminar normalmente
    if request.method == "POST":
        menu.delete()
        messages.success(request, "Menú eliminado correctamente.")
        return redirect('menus')
    
@login_required
def activar_desactivar_menu(request, menu_id):
    if request.user.rol not in [3, 4]:
        return HttpResponseForbidden("No tienes permiso para modificar este menú.")

    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == 'POST':
        menu.activo = not menu.activo
        menu.save()
        estado = "activado" if menu.activo else "desactivado"
        messages.success(request, f'Menú {estado} correctamente.')
        return redirect('menus')
    else:
        messages.error(request, 'Solicitud no permitida.')
        return redirect('menus')