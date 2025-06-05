from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from apps.registrar.models import CustomUser
from allauth.socialaccount.models import SocialAccount

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

        #si el usuario tiene socialaccount, no debe poder modificar su correo
        tiene_google = SocialAccount.objects.filter(user=user, provider='google').exists()
        
        #validar que el nombre de usuario no esté en uso
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            request.session['abrir_modal'] = True
            return redirect('perfil')

        #validar correo solo si puede modificarlo
        if not tiene_google:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Ese correo ya está registrado en otra cuenta.')
                request.session['abrir_modal'] = True
                return redirect('perfil')
            user.email = email
        else:
            #evita que lo cambie y muestra mensaje si intenta
            if email != user.email:
                messages.error(request, 'No puedes cambiar el correo porque iniciaste sesión con Google.')
                request.session['abrir_modal'] = True
                return redirect('perfil')

        #eliminar foto si se marcó la casilla
        if request.POST.get('eliminar_foto') == 'on' and user.foto_perfil:
            user.foto_perfil.delete()
            user.foto_perfil = None

        #subir nueva foto si se escogió
        if request.FILES.get('foto_perfil'):
            user.foto_perfil = request.FILES['foto_perfil']

        #actualizar otros datos
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = username
        user.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')

    return redirect('perfil')


#funciones admin
def es_admin(user):
    return user.is_authenticated and user.rol == 4

@login_required
@user_passes_test(es_admin)
def admin_usuarios(request):
    usuarios = CustomUser.objects.exclude(pk=request.user.pk)
    return render(request, 'perfil/admin_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin)
def cambiar_rol(request, user_id):
    usuario = get_object_or_404(CustomUser, pk=user_id)
    nuevo_rol = int(request.POST.get('nuevo_rol'))
    usuario.rol = nuevo_rol
    usuario.save()
    messages.success(request, 'Rol actualizado correctamente.')
    return redirect('admin_usuarios')

@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, pk=user_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('admin_usuarios')