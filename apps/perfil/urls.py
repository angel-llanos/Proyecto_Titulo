from django.urls import path
from . import views

urlpatterns = [
    path('', views.perfil , name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('admin-usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('cambiar-rol/<int:user_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]