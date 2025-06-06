from django.shortcuts import render

# Create your views here.
def reservas_mesero(request):
    context = { }
    return render(request, "reservas_mesero/reservas_mesero.html", context)
