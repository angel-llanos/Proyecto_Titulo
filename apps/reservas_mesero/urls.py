from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas_mesero, name='reservas_mesero'),

]