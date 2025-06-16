from apps.menus.models import Menu
from django.shortcuts import render

# Create your views here.
def index(request):
    menus = Menu.objects.filter(activo=True)[:3]
    return render(request, "home/index.html", {'menus': menus})