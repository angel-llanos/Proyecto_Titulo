from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar , name='registrar'),
    path('exit', views.exit , name="exit"),
]