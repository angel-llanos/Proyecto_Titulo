from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_empleado, name='crear_empleado'),
]