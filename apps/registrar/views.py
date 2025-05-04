from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomPasswordResetForm
from django.urls import reverse_lazy
from .models import CustomUser

def exit(request):
    logout(request)
    return redirect('index')

def registrar(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()
    active_tab = 'login'

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('index')
            else:
                active_tab = 'login'

        elif 'register_submit' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()

                backend = get_backends()[0]  # Usa el primer backend definido
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Formulario inválido.")
                active_tab = 'register'

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab,
    }

    return render(request, 'registrar/registrar.html', context)


class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = 'registration/password_reset_email_html.html'  # Asegúrate de que este archivo exista
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        # Validar si el correo está registrado en la base de datos
        if not CustomUser.objects.filter(email=email).exists():
            form.add_error('email', 'El correo electrónico no está registrado.')
            return self.form_invalid(form)
        
        return super().form_valid(form)