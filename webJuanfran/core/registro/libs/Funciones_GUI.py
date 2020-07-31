import threading
from tkinter import messagebox
from core.registro.libs.bot import *
import time

def salirAplicacion(root):
	valor = messagebox.askokcancel("Salir","¿Deseas salir de la aplicación?")
	if valor is True:
		root.destroy()

def inicioRegistro(inicioBot):
	path = "Z:/Bot/Acciones.txt"
	inicio = False
	if os.path.isfile(path):
		inicio = True
		inicio_ArchivosBot()
		hilo1 = threading.Thread(target = bot, args = (), daemon=True)
		if inicioBot:
			hilo1.start()
			print("iniciando registro")
	else:
		print("Ordenador no conectado en red")
	return inicio

def finRegistro():
	sec = time.time()
	path = "Z:/Bot/Registro.txt"
	fin = False
	#Escribo el final de la sesion en el registro.
	if os.path.isfile(path):
		fin = True
		archivo = open(path, "a")
		archivo.write(f"Fin Sesion: {time.ctime(sec)}\n"
			"-------------------------------------------------------------------\n")
		archivo.close()
		#Reinicio los archivos que usa el bot.
		path = "core/registro/files/bot.txt"
		archivo = open(path, "w")
		archivo.write("END_REGISTRO")
		archivo.close()

		path = "Z:/Bot/Acciones.txt"
		archivo = open(path, "w")
		archivo.write("END_REGISTRO")
		archivo.close()
		print("Fin registro")
		#root.destroy()
	else:
		print("ordenador no conectado en red")

	return fin

def vacio():
	pass

def inicio_ArchivosBot():
	sec = time.time()
	#Reinicio los archivos que usa el bot.
	path = "core/registro/files/bot.txt"
	archivo = open(path, "w")
	archivo.close()

	path = "Z:/Bot/Acciones.txt"
	if os.path.isfile(path):
		archivo = open(path, "w")
		archivo.write("Table_X:INI:25\n")
		archivo.close()
	print("Fin registro")
	#Escribo el final de la sesion en el registro.
	path = "Z:/Bot/Registro.txt"
	archivo = open(path, "a")
	archivo.write(f"Inicio Sesion: {time.ctime(sec)}\n"
		f"-------------------------------------------------------------------\n")
	archivo.close()

	