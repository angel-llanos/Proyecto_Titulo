from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_backends
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount

# Create your views here.
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

                backend = get_backends()[0]
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
    html_email_template_name = 'registration/password_reset_email_html.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    extra_context = {}

    def form_valid(self, form):
        
        email = form.cleaned_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            form.add_error('email', 'El correo electrónico no está registrado.')
            return self.form_invalid(form)

        # aquí verifica si el usuario tiene cuenta con google
        if SocialAccount.objects.filter(user=user, provider='google').exists():
            form.add_error('email', 'Esta cuenta está registrada mediante inicio con Google. No puedes recuperar la contraseña aquí.')
            return self.form_invalid(form)

        # si sale bien, se muestra correo enviado
        self.extra_context = {'is_google_account': False}
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context