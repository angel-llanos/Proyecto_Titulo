from django.shortcuts import render

# Create your views here.
def perfil(request):
    context = { }
    return render(request, "perfil/perfil.html", context)