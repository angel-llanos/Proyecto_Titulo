from django.shortcuts import render
from apps.reservas.models import Reserva

# Vista para mostrar todas las reservas de todos los usuarios al cocinero
def reservas_cocinero(request):
    reservas = Reserva.objects.select_related('cliente').order_by('-fecha', '-hora')
    return render(request, 'reservas_cocinero/reservas_cocinero.html', {
        'reservas': reservas
    })