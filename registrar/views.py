from django.shortcuts import render

def registrar(request):
    context = { }
    return render(request, "registrar/registrar.html", context)