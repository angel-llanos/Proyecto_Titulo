from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas, name='reservas'),  # Vista general o landing de reservas
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('elegir-mesas/<str:reserva_id>/', views.elegir_mesas, name='elegir_mesas'),
    path('exito/<str:reserva_id>/', views.reserva_exito, name='reserva_exito'),
]
