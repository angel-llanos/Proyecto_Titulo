from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas_cocinero, name='reservas_cocinero'),

]