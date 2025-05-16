from django.shortcuts import render, redirect, get_object_or_404
from apps.reservas.forms import ReservaForm
from django.contrib.auth.decorators import login_required
from .models import Reserva, Mesa
from decimal import Decimal

# Create your views here.
def reservas(request):
    context = { }
    return render(request, "reservas/reservas.html", context)

ABONO_PORCENTAJE = Decimal('0.3')

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user
            comensales = form.cleaned_data['comensales']
            menu = form.cleaned_data['menu']
            if menu:
                total = menu.precio * comensales
                reserva.abono = total * ABONO_PORCENTAJE  # 30%
            else:
                reserva.abono = 0
            reserva.estado = 'borrador'  # aún no ha elegido mesas
            reserva.save()
            return redirect('elegir_mesas', reserva_id=reserva.id_reserva)
    else:
        form = ReservaForm()

    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def elegir_mesas(request, reserva_id):
    reserva = get_object_or_404(Reserva, id_reserva=reserva_id, cliente=request.user)
    fecha = reserva.fecha
    hora = reserva.hora
    zona = reserva.zona

    mesas_ocupadas = Mesa.objects.filter(
        reserva__fecha=fecha,
        reserva__hora=hora,
        reserva__zona=zona
    ).distinct()

    mesas_disponibles = Mesa.objects.filter(zona=zona).exclude(id__in=mesas_ocupadas)

    if request.method == "POST":
        mesas_seleccionadas_ids = request.POST.getlist('mesas')
        if not mesas_seleccionadas_ids:
            error = "Debes seleccionar al menos una mesa."
            return render(request, 'reservas/elegir_mesas.html', {
                'reserva': reserva,
                'mesas_disponibles': mesas_disponibles,
                'error': error
            })

        reserva.mesas.clear()
        for mesa_id in mesas_seleccionadas_ids:
            mesa = Mesa.objects.get(id=mesa_id)
            reserva.mesas.add(mesa)

        reserva.estado = 'completada'  # Aquí se actualiza
        reserva.save()

        return redirect('reserva_exito', reserva_id=reserva.id_reserva)

    return render(request, 'reservas/elegir_mesas.html', {
        'reserva': reserva,
        'mesas_disponibles': mesas_disponibles,
    })

def reserva_exito(request, reserva_id):
    # Buscar por el campo personalizado alfanumérico
    reserva = get_object_or_404(Reserva, id_reserva=reserva_id)

    context = {
        'reserva': reserva,
        'cliente': reserva.cliente,
    }
    return render(request, 'reservas/reserva_exito.html', context)
