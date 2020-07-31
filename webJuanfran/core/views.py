from django.shortcuts import render, HttpResponse
from core.registro.libs.Funciones_GUI import *

# Create your views here.

def home(request):
    return render(request, "core/home.html")

def register(request):
    return render(request, "core/registro.html")

def start(request):
    inicio = inicioRegistro(True)

    return render(request, "core/registro_start.html", {"inicio":inicio})

def stop(request):
    fin = finRegistro()
    #fin = True
    if fin:
        pagina = "core/registro.html"
    else:
        pagina = "core/registro_stop.html"

    return render(request, "core/registro_stop.html" , {"fin":fin})
