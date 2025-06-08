from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('elegir-mesas/<str:reserva_id>/', views.elegir_mesas, name='elegir_mesas'),

    # Mostrar resumen del checkout
    path('checkout/<str:reserva_id>/', views.reserva_checkout, name='reserva_checkout'),

    # Iniciar proceso de pago con Stripe
    path('iniciar-pago/<str:reserva_id>/', views.checkout, name='checkout'),

    path('exito/<str:reserva_id>/', views.reserva_exito, name='reserva_exito'),
    path('fallo/<str:reserva_id>/', views.reserva_fallo, name='reserva_fallo'),
    path('historial/', views.historial_reservas, name='historial_reservas'),
    path('historial-usuario/<int:usuario_id>/', views.historial_usuario_admin, name='historial_usuario_admin'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva_admin, name='cancelar_reserva_admin'),
]