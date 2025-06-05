from django.urls import path
from . import views

urlpatterns = [
    path('', views.menus, name='menus'),
    path('agregar/', views.agregar_menu, name='agregar_menu'),
    path('modificar/<int:menu_id>/', views.modificar_menu, name='modificar_menu'),
    path('eliminar/<int:menu_id>/', views.eliminar_menu, name='eliminar_menu'),
    path('menus/toggle_estado/<int:menu_id>/', views.activar_desactivar_menu, name='activar_desactivar_menu'),

]