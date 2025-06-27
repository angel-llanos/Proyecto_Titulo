from django.shortcuts import render
from apps.reservas.models import Reserva
from django.utils.timezone import now

# Vista para mostrar todas las reservas de todos los usuarios al mesero
def reservas_mesero(request):
    reservas_futuras = Reserva.objects.filter(fecha__gte=now().date()).order_by('fecha', 'hora')
    reservas_pasadas = Reserva.objects.filter(fecha__lt=now().date()).order_by('-fecha', '-hora')
    reservas = list(reservas_futuras) + list(reservas_pasadas)  # concatenar listas
    return render(request, 'reservas_mesero/reservas_mesero.html', {'reservas': reservas})