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

        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            request.session['abrir_modal'] = True
            return redirect('perfil')

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Ese correo ya está registrado en otra cuenta.')
            request.session['abrir_modal'] = True
            return redirect('perfil')

        # NUEVO: si se envió una foto, guardarla
        if request.FILES.get('foto_perfil'):
            user.foto_perfil = request.FILES['foto_perfil']

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = username
        user.email = email
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    return redirect('perfil')
