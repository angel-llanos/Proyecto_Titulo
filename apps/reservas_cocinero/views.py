from django.shortcuts import render
from apps.reservas.models import Reserva
from django.utils.timezone import now

# Vista para mostrar todas las reservas de todos los usuarios al cocinero
def reservas_cocinero(request):
    reservas_pasadas = Reserva.objects.filter(fecha__lt=now().date()).order_by('-fecha', '-hora')
    reservas_futuras = Reserva.objects.filter(fecha__gte=now().date()).order_by('fecha', 'hora')
    reservas = list(reservas_pasadas) + list(reservas_futuras)  # concatenar listas
    return render(request, 'reservas_cocinero/reservas_cocinero.html', {'reservas': reservas})