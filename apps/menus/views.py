from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu
from .forms import MenuForm
from django.contrib.auth.decorators import login_required

# Create your views here.
# Vista pública o general de menús
def menus(request):
    lista_menus = Menu.objects.all()
    context = {'menus': lista_menus}
    return render(request, 'menus/menus.html', context)

# Vista para agregar un nuevo menú (solo administrador)
@login_required
def agregar_menu(request):
    if request.user.rol != 4:  # Solo rol 4 (Administrador)
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
    # Solo administrador (rol 4) por ahora
    if request.user.rol != 4:
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
    # Solo admin por ahora (rol 4)
    if request.user.rol != 4:
        return HttpResponseForbidden("No tienes permiso para eliminar este menú.")

    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == 'POST':
        menu.delete()
        messages.success(request, 'Menú eliminado correctamente.')
        return redirect('menus')
    else:
        # Si no es POST, no se elimina, redirige o muestra error
        messages.error(request, 'Solicitud no permitida.')
        return redirect('menus')