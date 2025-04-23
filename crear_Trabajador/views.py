from django.shortcuts import render

# Create your views here.

def crear_Trabajador(request):
    context = { }
    return render(request, "crear_Trabajador/crear_Trabajador.html", context)
