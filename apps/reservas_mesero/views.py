from django.shortcuts import render
from apps.reservas.models import Reserva

# Vista para mostrar todas las reservas de todos los usuarios
def reservas_mesero(request):
    reservas = Reserva.objects.select_related('cliente').order_by('-fecha', '-hora')
    return render(request, 'reservas/historial_usuario_admin.html', {
        'reservas': reservas
    })