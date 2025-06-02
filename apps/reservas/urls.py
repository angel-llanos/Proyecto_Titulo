from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas, name='reservas'),  # Landing de reservas
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('elegir-mesas/<str:reserva_id>/', views.elegir_mesas, name='elegir_mesas'),
    path('exito/<str:reserva_id>/', views.reserva_exito, name='reserva_exito'),
    path('historial/', views.historial_reservas, name='historial_reservas'),
    path('historial-usuario/<int:usuario_id>/', views.historial_usuario_admin, name='historial_usuario_admin'),
]
