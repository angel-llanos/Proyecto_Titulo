from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .forms import ContactoForm

def contacto(request):
    enviado = False

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            correo = form.cleaned_data['correo']
            razon = form.cleaned_data['razon']

            asunto = f"Nuevo mensaje de contacto de {nombre} {apellido}"
            mensaje = f"""
            Has recibido un nuevo mensaje desde el formulario de contacto:

            Nombre: {nombre}
            Apellido: {apellido}
            Correo: {correo}

            Mensaje:
            {razon}
            """

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            enviado = True
            form = ContactoForm()  # Limpia el formulario después del envío
    else:
        form = ContactoForm()

    return render(request, 'contacto/contacto.html', {'form': form, 'enviado': enviado})