from django.urls import path
from . import views

urlpatterns = [
    path('', views.historia , name='historia'),
]