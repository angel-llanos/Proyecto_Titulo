from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

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
