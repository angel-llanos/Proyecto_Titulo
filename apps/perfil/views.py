from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.
def perfil(request):
    context = { }
    return render(request, "perfil/perfil.html", context)

User = get_user_model()

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Validar que el username no esté en uso por otro usuario
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            request.session['abrir_modal'] = True
            return redirect('perfil')

        # Validar que el email no esté en uso por otro usuario
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Ese correo ya está registrado en otra cuenta.')
            request.session['abrir_modal'] = True
            return redirect('perfil')

        # Eliminar foto si se marcó la opción
        if request.POST.get('eliminar_foto') == 'on' and user.foto_perfil:
            user.foto_perfil.delete()
            user.foto_perfil = None

        # Subir nueva foto si se proporcionó
        if request.FILES.get('foto_perfil'):
            user.foto_perfil = request.FILES['foto_perfil']

        # Actualizar otros datos
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    return redirect('perfil')
