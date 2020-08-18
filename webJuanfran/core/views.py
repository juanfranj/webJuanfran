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

def automaticRegister(request):
    comenzar = False
    diccionario = {}
    if  len(request.GET) > 1 and request.GET["mesas"] != "" and len(request.GET["torneos"])>0:
        comenzar = True
        for i in request.GET.getlist("torneos"):
            print(i)
        diccionario = {"comenzar":comenzar, "torneos":request.GET.getlist("torneos"), "mesas":request.GET["mesas"], "datos":request.GET, "tamaño":len(request.GET)}
    return render(request, "core/registroAutomatico.html", diccionario)

def registroManual(request):
    escribir_registro()
    return render(request, "core/registroAutomatico.html")

def escribir_registro():
    try:
        path = "Z:/Bot/Acciones.txt"
        archivo = open(path, "a")
    except:
        path = "C:/Capturador/Bot/Acciones.txt"
        archivo = open(path, "a")
    archivo.write(f"\nREGISTRO")