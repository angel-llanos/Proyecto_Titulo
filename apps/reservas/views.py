import base64
from django.templatetags.static import static
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.urls import reverse
from apps.registrar.models import CustomUser
from .forms import ReservaForm
from .models import Reserva, Mesa
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Q
import stripe
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib import messages
from django.utils.timezone import now
stripe.api_key = settings.STRIPE_SECRET_KEY

def reservas(request):
    return redirect('crear_reserva')

@login_required
def crear_reserva(request):
    reserva_borrador = Reserva.objects.filter(cliente=request.user, estado='borrador').first()

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva_borrador)
        if form.is_valid():
            menu = form.cleaned_data.get('menu')
            comensales = int(form.cleaned_data.get('comensales'))
            abono = Decimal('4000') * comensales

            # Manejo de total dependiendo si se seleccionó un menú o no
            if menu:
                total = (menu.precio * comensales) - abono
            else:
                # Por ejemplo, si no hay menú, solo se cobra el abono como total
                total = abono

            reserva = form.save(commit=False)
            reserva.cliente = request.user
            reserva.abono = abono
            reserva.total = total
            reserva.estado = 'borrador'
            reserva.save()

            messages.success(request, f'Reserva #{reserva.id} creada para {reserva.cliente.username}')
            request.session['reserva_timestamp'] = now().timestamp()

            request.session['reserva_id'] = reserva.id
            request.session['reserva_datos'] = {
                'nombre_reserva': reserva.nombre_reserva,
                'fecha': str(reserva.fecha),
                'hora': str(reserva.hora),
                'telefono': reserva.telefono,
                'zona_id': reserva.zona.id,
                'menu_id': reserva.menu.id if reserva.menu else None,
                'comensales': reserva.comensales,
                'abono': str(abono),
                'total': str(total)
            }

            return redirect('elegir_mesas', reserva_id=reserva.id)
    else:
        form = ReservaForm(instance=reserva_borrador)

    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def elegir_mesas(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    zona = reserva.zona
    fecha = reserva.fecha
    hora = reserva.hora
    comensales = reserva.comensales

    hora_inicio = datetime.combine(fecha, hora)
    hora_fin = hora_inicio + timedelta(hours=2)
    hora_limite_inferior = hora_inicio - timedelta(hours=2)

    reservas_solapadas = Reserva.objects.filter(
        fecha=fecha,
        zona=zona
    ).exclude(id=reserva.id).filter(
        Q(hora__gte=hora_limite_inferior.time(), hora__lt=hora_fin.time())
    )

    mesas_ocupadas_ids = Mesa.objects.filter(
        reserva__in=reservas_solapadas
    ).values_list('id', flat=True)

    mesas = Mesa.objects.filter(zona=zona).all()
    for mesa in mesas:
        mesa.disponible = mesa.id not in mesas_ocupadas_ids

    # Asignar URL de imagen según la zona
    if zona.nombre == 'Patio':
        img_url = static('reservas/img/patio.png')
    elif zona.nombre == 'Primer Piso':
        img_url = static('reservas/img/piso1.png')
    elif zona.nombre == 'Segundo Piso':
        img_url = static('reservas/img/piso2.png')
    else:
        img_url = static('reservas/img/default.png')

    # Aquí debes definir manualmente la posición de cada mesa en porcentaje
    # para que se posicionen correctamente sobre la imagen de fondo.
    if zona.nombre == 'Primer Piso':
        posiciones = {
            1: (47, 43),
            2: (22, 26),
            3: (75, 27),
            4: (73, 54),
            5: (57, 72),
            6: (27, 75),
        }
    elif zona.nombre == 'Segundo Piso':
        posiciones = {
            7: (51, 70),
            8: (22, 77),
            9: (75, 62),
            10: (75, 27),
            11: (49, 44),
            12: (24, 26),
        }
    elif zona.nombre == 'Patio':
        posiciones = {
            17:  (45, 70),
            14:  (72, 30),
            15:  (23, 65),
            16: (25, 33),
            13: (51, 44),
            18: (69, 73),
        }
    else:
        posiciones = {}

    for mesa in mesas:
        pos = posiciones.get(mesa.numero, (0, 0))
        mesa.pos_x = pos[0]
        mesa.pos_y = pos[1]

    if request.method == "POST":
        mesas_seleccionadas_ids = request.POST.getlist('mesas')
        mesas_seleccionadas = Mesa.objects.filter(id__in=mesas_seleccionadas_ids)
        capacidad_total = sum(mesa.capacidad for mesa in mesas_seleccionadas)

        if not mesas_seleccionadas:
            error = "Debes seleccionar al menos una mesa."
        elif any(int(mesa.id) in mesas_ocupadas_ids for mesa in mesas_seleccionadas):
            error = "Una o más mesas seleccionadas ya no están disponibles."
        elif capacidad_total < comensales:
            error = f"La capacidad total de las mesas seleccionadas ({capacidad_total}) no cubre los {comensales} comensales."
        elif capacidad_total > comensales + 2 and len(mesas_seleccionadas) > 1:
            error = f"La capacidad total de las mesas seleccionadas ({capacidad_total}) excede demasiado los {comensales} comensales. Reduce la cantidad de mesas."
        else:
            reserva.mesas.set(mesas_seleccionadas)
            reserva.estado = 'pendiente_pago'
            reserva.save()
            request.session.pop('reserva_id', None)
            request.session.pop('reserva_datos', None)
            return redirect('reserva_checkout', reserva_id=reserva.id)

        return render(request, 'reservas/elegir_mesas.html', {
            'mesas': mesas,
            'reserva': reserva,
            'capacidades_disponibles': sorted(set(m.capacidad for m in mesas)),
            'error': error,
            'img_url': img_url,
        })

    return render(request, 'reservas/elegir_mesas.html', {
        'mesas': mesas,
        'reserva': reserva,
        'capacidades_disponibles': sorted(set(m.capacidad for m in mesas)),
        'img_url': img_url,
    })

@login_required
def reserva_checkout(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    if request.method == 'POST':
        # 1) Validar checkbox
        if not request.POST.get('acepta_terminos'):
            messages.error(request, "Debes aceptar los términos y condiciones para continuar.")
            return redirect('reserva_checkout', reserva_id=reserva_id)

        # 2) Redirigir a checkout (ahí crearemos la sesión)
        return redirect('checkout', reserva_id=reserva.id)

    # GET: mostrar form con el checkbox
    return render(request, 'reservas/reserva_checkout.html', {'reserva': reserva})

#checkout de stripe
@login_required
def checkout(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user)

    try:
        # Armar URLs de éxito y cancelación
        success_url = request.build_absolute_uri(
            reverse('reserva_exito', args=[reserva.id])
        )
        cancel_url = request.build_absolute_uri(
            reverse('reserva_fallo', args=[reserva.id])
        )

        # Crear sesión de Stripe y redirigir al checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'clp',
                    'unit_amount': int(reserva.abono),
                    'product_data': {
                        'name': f'Reserva MonkeyFoods: {reserva.nombre_reserva}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'reserva_id': reserva.id,
                'cliente_id': request.user.id
            }
        )
        return redirect(checkout_session.url)

    except Exception as e:
        # Log en consola y mensaje amigable
        print("Error en Stripe:", e)
        messages.error(request, "Ocurrió un error al procesar el pago. Intenta nuevamente.")
        return redirect('reserva_fallo', reserva_id=reserva.id)

def reserva_exito(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if reserva.estado != 'completada':
        reserva.estado = 'completada'
        reserva.save()

        # Enviamos la boleta por correo automáticamente
        enviar_boleta_por_correo(reserva)

    return render(request, 'reservas/reserva_exito.html', {
        'reserva': reserva,
        'cliente': reserva.cliente,
    })

def reserva_fallo(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'reservas/reserva_fallo.html', {
        'reserva': reserva,
        'cliente': reserva.cliente,
    })

#historial de reservas
@login_required
def historial_reservas(request):
    
    hoy = now().date()

    # Reservas desde hoy en adelante (ordenadas de más cercana a más lejana)
    reservas_futuras = Reserva.objects.filter(
        cliente=request.user,
        fecha__gte=hoy
    ).order_by('fecha', 'hora')

    # Reservas anteriores a hoy (ordenadas de más reciente a más antigua)
    reservas_pasadas = Reserva.objects.filter(
        cliente=request.user,
        fecha__lt=hoy
    ).order_by('-fecha', '-hora')

    # Juntamos ambas listas: futuras primero
    reservas = list(reservas_futuras) + list(reservas_pasadas)

    return render(request, 'reservas/historial_reservas.html', {'reservas': reservas})

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

#cancelar reserva
@user_passes_test(es_admin)
def cancelar_reserva_admin(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if reserva.estado != 'cancelada':
        reserva.estado = 'cancelada'
        reserva.mesas.clear()
        reserva.save()
    return redirect('historial_usuario_admin', usuario_id=reserva.cliente.id)

#exportar en pdf
def generar_boleta_pdf(reserva):
    template = get_template('reservas/boleta_pdf.html')
    html = template.render({'reserva': reserva})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

def enviar_boleta_por_correo(reserva):
    pdf_content = generar_boleta_pdf(reserva)
    if pdf_content:
        email = EmailMessage(
            subject='Boleta de tu reserva en MonkeyFoods',
            body='Gracias por tu reserva. Adjuntamos tu boleta en PDF.',
            from_email=settings.EMAIL_HOST_USER,
            to=[reserva.cliente.email],
        )
        email.attach(f'boleta_{reserva.id}.pdf', pdf_content, 'application/pdf')
        email.send()

@login_required
def descargar_boleta(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # Validación de permisos
    if request.user != reserva.cliente:
        return HttpResponse("No tienes permiso para acceder a esta boleta", status=403)

    # Codificar imagen logo en base64
    with open('static/img/logo.png', 'rb') as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    html = render_to_string('reservas/boleta_pdf.html', {
        'reserva': reserva,
        'logo_base64': logo_base64,
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{reserva.id}.pdf"'

    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')

    return response