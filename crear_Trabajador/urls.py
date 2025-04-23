from django.urls import path
from . import views

urlpatterns = [
    path('crear_Trabajador/', views.crear_Trabajador, name='crear_Trabajador'),
]