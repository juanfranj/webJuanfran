# softwre para el bot.
import multiprocessing
import threading
import queue
import pyautogui as auto
import re
import os
import math
from time import sleep, time
from multiprocessing import Process , Queue
from random import randint, uniform
from time import sleep
from libs.pyclick import HumanClicker

def leerArchivo(cola):
	
	path = "Z:/Bot/Acciones.txt"
	while not os.path.isfile(path):
		sleep(0.1)
	archivo = open(path, "r")
	fin = False
	while not fin:
		linea = archivo.readline()
		if "END_REGISTRO" in linea:
			fin = True
		elif len(linea) > 0:
			cola.put(linea.replace("\n", ""))
		sleep(1)
	while(cola.empty() is False):
		sleep(1)
	archivo.close()
	print("Fin lectura")

def leerCola(cola):
	
	while True:
		if not cola.empty():
			#print("El tamaño de la cola es:", cola.qsize())
			ejecutarAccion(cola.get())
		else:
			#print("Cola Vacia")
			sleep(0.5)
		

def ejecutarAccion(accion):
	posicion, accion, mesa = acciones(accion)
	#if posicion[0] < 2000:
		#actuar(posicion, accion)
	actuar(posicion, accion, mesa)
		#print(posicion, accion)

def acciones(actuar):

	acciones = actuar.split(":")
	mesa = acciones[0]
	posicion = encontrarMesa(mesa)
	acciones.pop(0)

	return posicion, acciones, mesa

def encontrarMesa(mesa):

	if mesa == "Table_1":
		try :
			path = "Z:/Tables/Table_1/Posicion.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()
		except:
			print("Error posicion mesa 1")
			path = "Z:/Bot/posiciones/Posicion_table1.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()

	elif mesa == "Table_2":
		try:
			path = "Z:/Tables/Table_2/Posicion.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()
		except:
			print("Error posicion mesa 2")
			path = "Z:/Bot/posiciones/Posicion_table2.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()

	elif mesa == "Table_3":
		try:
			path = "Z:/Tables/Table_3/Posicion.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()
		except:
			print("Error posicion mesa 3")
			path = "Z:/Bot/posiciones/Posicion_table3.txt"
			archivo = open(path, "r")
			posicion = (archivo.readline()).split(",")
			x = int(posicion[0]) + randint(490,630) + 1920
			y = int(posicion[1]) + randint(136, 275)
			archivo.close()

	elif mesa == "Table_X":
		x = randint(500,1000)
		y = randint(500, 700)
	else:
		x, y = [2000, 2000]

	return [x, y]

def distancia(x, y):
    xini, yini = auto.position()
    #print("Punto incicial: ", xini, yini)
    distancia = math.sqrt((xini-x)**2+(yini-y)**2)
    return distancia

def actuar(pos, accion,mesa):

	x, y = pos
	xini, yini = [randint(1400, 1750), randint(600, 850)] 
	tipo = [auto.easeInQuad, auto.easeOutQuad, auto.easeInOutQuad, auto.easeOutQuad]
	auto.FAILSAFE = False
	#---------------Muevo el raton con pyclick que genera una curva Beizer---------------
	ini_total = time()
	hc = HumanClicker()
	if (distancia(x, y) > 100):
		ini = time()
		tiempo = uniform(0.2, 0.8)
		hc.move((x, y), tiempo)
		fin = time() - ini
		print("Mover raton real: ", fin)
		print("Mover raton seleccionado: ", tiempo)
	ini = time()
	hc.real_click()
	fin = time() - ini
	print("Click raton : ", fin)
	#---------------Se mueve el raton con autoguy directamente---------------------------
	#auto.moveTo(xini, yini, uniform(0.2,0.6), tipo[randint(0,3)])
	#auto.moveTo(x, y, uniform(0.25,0.5), tipo[randint(0,3)])
	#auto.click(button = "left", duration = 0.2)
	#------------------------------------------------------------------------------------
	#--------------------------------Actuar----------------------------------------------
	ini = time()
	accionDepurada(accion, mesa)
	fin = time() - ini
	print("Pulsar Tecla : ", fin)
	##########################################################
	#auto.moveTo(xini, yini, uniform(0.2,0.65), tipo[randint(0,3)])
	ini = time()
	hc.aleatorio()
	fin = time() - ini
	print("Aleatorio raton : ", fin)
	print("Total: ", time()-ini_total)
	print("Posicion ventana: ", pos, "Accion: ", accion)



def accionDepurada(accion,mesa):
	#print(accion)
	path = "Z:/Bot/Registro.txt"
	registro = open(path, "a")
	sleep(23 / randint(93,201))
	try:
		#-------------------------PRE-FLOP--------------------------------------------------#
		if "OR" in accion[0]:
			#auto.click(button = "left", duration = 0.2)
			registro.write("Accion = OR presiona: e\n")
			auto.press("e")
		elif "LIMP" in accion[0]:
			registro.write("Accion = LIMP presiona: w\n")
			auto.press("w")
		###############################################
		elif "RAISE" in accion[0]:

			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = RAISE presiona: {calculoISO(accion)}\n")
			auto.press(calculoISO(accion))

		###############################################
		elif "OS" in accion[0]:
			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = OS presiona: z\n")
			auto.press("z")

		elif "f" in accion[0] or "FOLD" in accion[0]:
			registro.write(f"Accion = FOLD presiona: boton derecho\n")
			auto.click(button = "right", duration = 0.2)

		elif "CHECK" in accion[0]:
			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = CHECK presiona: w\n")
			auto.press("w")

		elif "3BNAI" in accion[0]:

			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = 3BNAI presiona: x\n")
			auto.press("x")

		elif "3BAI" in accion[0]:

			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = 3BAI presiona: z\n")
			auto.press("z")

		elif "AI" in accion[0]:

			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = AI presiona: z\n")
			auto.press("z")

		#---------------------------POST-FOP-----------------------------------------------#

		elif "c" in accion[0] or "CALL" in accion[0]:
			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = CHECK presiona: w\n")
			auto.press("w")

		elif "f" in accion[0] or "FOLD" in accion[0]:
			registro.write(f"Accion = FOLD presiona: f\n")
			auto.click(button = "right", duration = 0.2)

		elif "b" in accion[0]:
			
			#auto.click(button = "left", duration = 0.2)
			registro.write(f"Accion = BET presiona: {calculoBet(accion, mesa)}\n")
			auto.press(calculoBet(accion, mesa))
	except:
		print("Error al pulsar tecla")

	registro.close()

def calculoBet(accion,mesa):
	
	#[40%, 58%, 74%, 120%, all-in]
	letras = ["a", "s", "d", "x", "z"]
	bet = int("".join(accion[0])[1:])
	bote = int(accion[-1])
	porc = (bet/bote) * 100
	#ai = calculoAI(mesa)
	ai = False;

	if ai == True:
		pulsar = letras[4]
	elif porc <= 49:
		pulsar = letras[0]
	elif porc <= 62:
		pulsar = letras[1]
	elif porc <= 90:
		pulsar = letras[2]
	elif porc <= 140:
		pulsar = letras[3]
	elif porc > 140:
		pulsar = letras[4]
	return pulsar


def calculoAI(mesa, bet):
	ai = False
	path = f"Z:/Tables/{mesa}/POSTFLOP/estrategia.txt"
	archivo=open(path ,"r")
	lineas = archivo.readlines()
	archivo.close()
	#stack efectivo
	stack_efectivo = int(lineas[1].replace("\n",""))
	#apuesta AI
	path = "Z:/Bot/Apuesta/apuesta.txt"
	archivo = open(path, "r")
	apuesta = int(archivo.readline())
	archivo.close()
	if apuesta > 0.7 * stack_efectivo:
		ai = True
	return ai

def calculoISO(accion):

	#[2.5bb, 2.7bb, 3bb, 3.5bb]
	letras = ["a", "s", "d", "x"]
	ciegas = int(accion[-1])
	if ciegas <= 10:
		iso = letras[0]
	elif ciegas <= 13:
		iso = letras[1]
	elif ciegas <= 19:
		iso = letras[2]
	elif ciegas > 19:
		iso = letras[3]
	return iso

def fin(t1, t2):
	path = "./files/bot.txt"
	while not os.path.isfile(path):
		sleep(0.1)
	archivo = open(path, "r")
	fin = False
	while not fin:
		linea = archivo.readline()
		if "END_REGISTRO" in linea:
			fin = True
		sleep(0.1)
	print("Fin Bot")


def bot():
	#cola = multiprocessing.Queue()
	cola = queue.Queue()
	t1 = threading.Thread(target = leerArchivo, args = (cola, ), daemon=True)
	t2 = threading.Thread(target = leerCola, args = (cola,), daemon=True)
	t1.start()
	t2.start()
	fin(t1, t2)
	

def crearArchivo():
	sleep(1)
	archivo = open("Z:/Bot/Acciones_.txt", "r")
	fin = False
	while not fin:
		copiar = open(("Z:/Bot/Acciones.txt"), "a")
		linea = archivo.readline()
		#print(linea)
		if "END_REGISTRO" in linea:
			fin = True
		copiar.write(linea)
		copiar.close()
		sleep(3)
	archivo.close()
	
def bot_Pruebas():
	print("Bot Comenzando")
	path = "./files/bot.txt"
	archivo = open(path, "w")
	archivo.close()

	path = "Z:/Bot/Acciones.txt"
	archivo = open(path, "w")
	archivo.close()

	path = "Z:/Bot/Registro.txt"
	registro = open(path, "w")
	archivo.close()

	#bot()
	hilo = threading.Thread(target = bot, args = ())
	#p3 = multiprocessing.Process(target = bot, args = ())
	hilo.start()

	hilo2 = threading.Thread(target = crearArchivo, args = ())
	hilo2.start()
	#p1 = multiprocessing.Process(target = bot, args = ())
	#p1.start()
"""
if __name__ == "__main__":

	print("Bot Comenzando")
	path = "./files/bot.txt"
	archivo = open(path, "w")
	archivo.close()

	path = "Z:/Bot/Acciones.txt"
	archivo = open(path, "w")
	archivo.close()

	path = "Z:/Bot/Registro.txt"
	registro = open(path, "w")
	archivo.close()

	#bot()
	hilo = threading.Thread(target = bot, args = ())
	#p3 = multiprocessing.Process(target = bot, args = ())
	hilo.start()

	hilo2 = threading.Thread(target = crearArchivo, args = ())
	hilo2.start()
	#p1 = multiprocessing.Process(target = bot, args = ())
	#p1.start()
"""