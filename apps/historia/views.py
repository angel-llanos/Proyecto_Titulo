from django.shortcuts import render

# Create your views here.
def historia(request):
    context = { }
    return render(request, "historia/historia.html", context)