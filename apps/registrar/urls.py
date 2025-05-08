from django.urls import path

from apps.perfil.views import perfil
from . import views

urlpatterns = [
    path('', views.registrar , name='registrar'),
    path('exit', views.exit , name="exit"),
]