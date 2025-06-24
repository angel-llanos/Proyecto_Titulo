from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('terminos_condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
]