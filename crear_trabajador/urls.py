from django.urls import path
from . import views

urlpatterns = [
    path('crear_trabajador/', views.crear_trabajador, name='crear_trabajador'),
]