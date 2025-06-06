"""
URL configuration for monkeyfoods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from django.urls import path, include # type: ignore
from apps.registrar.views import CustomPasswordResetView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # urls de apps de monkeyfoods
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('registrar/',include('apps.registrar.urls')),
    path('crear_empleado/',include('apps.crear_empleado.urls')),
    path('historia/',include('apps.historia.urls')),
    path('perfil/',include('apps.perfil.urls')),
    path('reservas/',include('apps.reservas.urls')),
    path('menus/',include('apps.menus.urls')),
    path('reservas_mesero/',include('apps.reservas_mesero.urls')),

    # urls de recuperación de contraseña
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # url de accounts, se utiliza para el login con google
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)