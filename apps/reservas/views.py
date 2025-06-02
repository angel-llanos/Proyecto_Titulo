from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.registrar.models import CustomUser
from .forms import ReservaForm
from .models import Reserva, Mesa
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Q

ABONO_PORCENTAJE = Decimal('0.3')

def reservas(request):
    return redirect('crear_reserva')

@login_required
def crear_reserva(request):
    # Buscar si ya existe reserva borrador para el usuario
    reserva_borrador = Reserva.objects.filter(cliente=request.user, estado='borrador').first()

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva_borrador)  # si hay borrador, editarlo
        if form.is_valid():
            menu = form.cleaned_data.get('menu')
            comensales = int(form.cleaned_data.get('comensales'))
            abono = ((menu.precio * ABONO_PORCENTAJE) * comensales) if menu else 0

            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.abono = abono
            reserva.estado = 'borrador'
            reserva.save()

            # Guardar en sesión el ID de reserva y datos
            request.session['reserva_id'] = reserva.id
            request.session['reserva_datos'] = {
                'nombre_reserva': reserva.nombre_reserva,
                'fecha': str(reserva.fecha),
                'hora': str(reserva.hora),
                'telefono': reserva.telefono,
                'zona_id': reserva.zona.id if reserva.zona else None,
                'menu_id': reserva.menu.id if reserva.menu else None,
                'comensales': reserva.comensales,
                'abono': str(abono),
            }

            return redirect('elegir_mesas', reserva_id=reserva.id)
    else:
        form = ReservaForm(instance=reserva_borrador)

    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def elegir_mesas(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    zona = reserva.zona
    menu = reserva.menu
    fecha = reserva.fecha
    hora = reserva.hora
    comensales = reserva.comensales

    # Combinar fecha y hora en un datetime completo
    hora_inicio = datetime.combine(fecha, hora)
    hora_fin = hora_inicio + timedelta(hours=2)
    hora_limite_inferior = hora_inicio - timedelta(hours=2)

    # Buscar reservas que se solapen en el rango de 2 horas (excepto la misma reserva actual)
    reservas_solapadas = Reserva.objects.filter(
        fecha=fecha,
        zona=zona
    ).exclude(id=reserva.id).filter(
        Q(
            hora__gte=hora_limite_inferior.time(),
            hora__lt=hora_fin.time()
        )
    )

    # Obtener los IDs de mesas ocupadas en esas reservas
    mesas_ocupadas_ids = Mesa.objects.filter(
        reserva__in=reservas_solapadas
    ).values_list('id', flat=True)

    mesas = Mesa.objects.filter(zona=zona).all()

    for mesa in mesas:
        mesa.disponible = (mesa.id not in mesas_ocupadas_ids) and (mesa.capacidad >= comensales)

    if request.method == "POST":
        mesas_seleccionadas_ids = request.POST.getlist('mesas')
        if not mesas_seleccionadas_ids:
            return render(request, 'reservas/elegir_mesas.html', {
                'mesas': mesas,
                'error': "Debes seleccionar al menos una mesa.",
                'reserva': reserva,
                'capacidades_disponibles': sorted(set(m.capacidad for m in mesas)),
            })

        # Actualizar la reserva existente
        reserva.mesas.set(Mesa.objects.filter(id__in=mesas_seleccionadas_ids))
        reserva.estado = 'completada'
        reserva.save()

        # Limpiar sesión
        request.session.pop('reserva_id', None)
        request.session.pop('reserva_datos', None)

        return redirect('reserva_exito', reserva_id=reserva.id)

    return render(request, 'reservas/elegir_mesas.html', {
        'mesas': mesas,
        'reserva': reserva,
        'capacidades_disponibles': sorted(set(m.capacidad for m in mesas)),
    })

def reserva_exito(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'reservas/reserva_exito.html', {
        'reserva': reserva,
        'cliente': reserva.cliente,
    })

@login_required
def historial_reservas(request):
    reservas = Reserva.objects.filter(cliente=request.user).order_by('-fecha', '-hora')
    return render(request, 'reservas/historial_reservas.html', {'reservas': reservas})

# funciones admin
def es_admin(user):
    return user.is_authenticated and user.rol == 4

@user_passes_test(es_admin)
def historial_usuario_admin(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    reservas = Reserva.objects.filter(cliente=usuario).order_by('-fecha', '-hora')
    return render(request, 'reservas/historial_usuario_admin.html', {
        'usuario': usuario,
        'reservas': reservas
    })