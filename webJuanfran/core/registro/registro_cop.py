import cv2
import numpy as np
import pytesseract
import pyautogui
from math import sqrt
from time import sleep
from libs.bot import *



def mostrarImagen(imagen):
    cv2.imshow("imagen", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def capturador_winamax(comenzar):
    comenzar = True
    while comenzar:
        ## capturo la pantalla para buscar el Lobby de winamax
        img = pyautogui.screenshot()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        ## busco el lobby
        loc, dim, lobby = obtener_lobby(frame)
        sleep(0.03)

def obtener_lobby(imagen):
    ## aplico los filtros para encontrar los bordes
    grayscale = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(grayscale, 80, 255,  cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    ret, thresh = cv2.threshold(opening, 100, 255,  cv2.THRESH_BINARY_INV)
    ## busco los contornos
    im2, contours,hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #img = cv2.drawContours(imagen, contours, -1, (0,0,255), 3)
    ## eligo el contorno con mayor superficie
    index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]),reverse=True)
    contours_sort = [contours[i] for i in index_sort]

    if len(contours_sort) > 1:
        contorno_maximo = contours_sort[0]
        (x,y,w,h) = cv2.boundingRect(contorno_maximo)
        # dibujamo el lobby
        #imagen = cv2.rectangle(imagen,(x,y),(x+w,y+h),(0,0,255),2)
        lobby = imagen[y:y+h, x:x+w] 
    #mostrarImagen(lobby)
    #mostrarImagen(img)
    return lobby, [x, y]

def obtener_mesas(imagen):
    ## aplico filtros para obtener el texto de las mesas
    
    grayscale = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(grayscale, 60, 255,  cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    ret, thresh = cv2.threshold(opening, 100, 255,  cv2.THRESH_BINARY_INV)
    ## busco los contornos
    im2, contours, hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #img = cv2.drawContours(imagen, contours, -1, (0,0,255), 3)
    #mostrarImagen(img)
    #mostrarImagen(thresh)
    ## ordeno por area
    index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]),reverse=True)
    contours_sort = [contours[i] for i in index_sort]
    
    ## para cada rectangulo, comprobamos que tenga las dimensiones de una mesa
    for contour in contours_sort:
        (x,y,w,h) = cv2.boundingRect(contour)
        if (w > 400 and w < 1000) and (h < w) and (h > 300):
            #img= cv2.rectangle(imagen,(x,y),(x+int(w*1),y+h),(0,0,255),2)# todas config             
            mesas = imagen[y:y+int(h/2), x:x+w]
            x_mesas, y_mesas = x, y
    #mostrarImagen(mesas)
    return mesas, [x_mesas, y_mesas]

def leerTexto(imagen):
    ## aplico los filtros para pasa ocr
    resize = cv2.resize(imagen, None,fx=3, fy=3, interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
    retval, chat = cv2.threshold(gray,175,255,1)
    ## configuracion de tesseract y pasar en imagen
    config = ('-l eng --oem 1 --psm 6')
    texto =  pytesseract.image_to_string(chat, config = config).split("\n") 
    ## simplifico el texto.
    texto_simplificado = simplificar_texto(texto)
    #mostrarImagen(chat)
    return texto_simplificado

def simplificar_texto(texto):
    texto_simplificado = []
    for linea in texto:
        linea = linea.split(" ")
        del linea[1:5] 
        texto_simplificado.append(" ".join(linea))
    return texto_simplificado

def buscar_mesa(texto):
    mesas = []
    posicion = 0
    for linea in texto:
        if "Open" in linea and "Heads" in linea and "0" in linea:
            mesas.append(posicion)
        posicion += 1
    return mesas

def localizacion_mesas(mesas_libres, mesas, posicion_mesas, posicion_lobby):
    h, w, c = mesas.shape
    fila = int(h) * 0.061
    x_lobby, y_lobby = posicion_lobby
    x_mesas, y_mesas = posicion_mesas
    posicion_y = None
    posicion_x = None
    if len(mesas_libres) > 0:
        posicion_y = int(mesas_libres[0] * fila + fila/2) + y_lobby + y_mesas
        posicion_x = int(w/2) + x_lobby + x_mesas
    return posicion_x, posicion_y

def escribir_localizacion(posicion_x, posicion_y):
    try:
        path = "Z:/Bot/Acciones.txt"
        archivo = open(path, "a")

    except:
        path = "C:/Capturador/Bot/Acciones.txt"
        archivo = open(path, "a")
    
    archivo.write(f"\nREGISTRO:{posicion_x}:{posicion_y}")

def buscar_registrar(imagen, posicion_lobby):
    #mostrarImagen(imagen)
    imagen = detectar_rojo(imagen)
    x_lobby, y_lobby = posicion_lobby
    ## aplico un filtro a la imagen para detectar los contornos
    c, W, H = imagen.shape[::-1]
    cartas = imagen
    grayscale = cv2.cvtColor(cartas, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayscale, 0, 255, 0)
    ## busco contornos
    im2, contours,hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ## ordeno por superficie esos contornos
    index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]),reverse=True)
    contours_sort = [contours[i] for i in index_sort]
    distancia = []
    if len(contours_sort) > 1:
        for i in range(len(contours)):
            size = cv2.contourArea(contours_sort[i])
            (x, y, w, h) = cv2.boundingRect(contours_sort[i])
            distancia.append(sqrt(x**2+y**2))
    ## ordeno por distancias
        index_sort_dist = sorted(range(len(contours)), key = lambda i: distancia[i])
        contours_sort_dist = [contours_sort[i] for i in index_sort_dist]
    else:
        contours_sort_dist = contours_sort
    ## para cada rectangulo, comprobamos que tenga las dimensiones de una carta
    botones = {}
    for contour in contours_sort_dist:
        #print ("Contorno: ", (cv2.contourArea(contour)))
        if cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 10000:
            (x,y,w,h) = cv2.boundingRect(contour)
            ## Condicion para ser boton de registrar
            if h < w/2 and y > H/4 and y < H/2: 
                imagen = cv2.rectangle(cartas,(x,y),(x+w,y+h),(255,0,0),2)
                valor = botones.get("registro",0)
                registro_x = x + x_lobby
                registro_y = y+ y_lobby
                botones["registro"] = [x + x_lobby, y+ y_lobby, w, h]
    #mostrarImagen(imagen)
    return botones

def detectar_rojo(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    #Rango de colores detectados:
    rojo_bajos1 = np.array([0,100,100], dtype=np.uint8)
    rojo_altos1 = np.array([10, 255, 255], dtype=np.uint8)
    rojo_bajos2 = np.array([170,100,100], dtype=np.uint8)
    rojo_altos2 = np.array([179, 255, 255], dtype=np.uint8)
    #Crear las mascaras
    mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
    mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
    mascara_rojos = cv2.add(mascara_rojo1, mascara_rojo2)
    mascaravis = cv2.bitwise_and(imagen, imagen, mask= mascara_rojos) 

    return mascaravis

def buscar_registrar_final(imagen, posicion_lobby):
    
    imagen = detectar_rojo(imagen)
    x_lobby, y_lobby = posicion_lobby
    ## aplico un filtro a la imagen para detectar los contornos
    c, W, H = imagen.shape[::-1]
    cartas = imagen
    grayscale = cv2.cvtColor(cartas, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayscale, 0, 255, 0)
    ## busco contornos
    im2, contours,hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ## ordeno por superficie esos contornos
    index_sort = sorted(range(len(contours)), key=lambda i : cv2.contourArea(contours[i]),reverse=True)
    contours_sort = [contours[i] for i in index_sort]
    distancia = []
    if len(contours_sort) > 1:
        for i in range(len(contours)):
            size = cv2.contourArea(contours_sort[i])
            (x, y, w, h) = cv2.boundingRect(contours_sort[i])
            distancia.append(sqrt(x**2+y**2))
    ## ordeno por distancias
        index_sort_dist = sorted(range(len(contours)), key = lambda i: distancia[i])
        contours_sort_dist = [contours_sort[i] for i in index_sort_dist]
    else:
        contours_sort_dist = contours_sort
    ## para cada rectangulo, comprobamos que tenga las dimensiones de una carta
    botones = {}
    for contour in contours_sort_dist:
        if cv2.contourArea(contour) > 400 and cv2.contourArea(contour) < 10000:
            (x,y,w,h) = cv2.boundingRect(contour)
            ## Condicion para ser boton de registrar final
            if h < w/2 and y > H/2 and x < W/2: 
                imagen = cv2.rectangle(cartas,(x,y),(x+w,y+h),(255,0,0),2)
                valor = botones.get("registro",0)
                botones["registro"] = [x + x_lobby, y+ y_lobby, w, h]
    #print(botones)
    #mostrarImagen(imagen)
    return botones


def registrarSit():
    registrar = True
    try:
        pantalla = capturarPantalla()
        lobby, posicion_lobby = obtener_lobby(pantalla)
        mesas, posicion_mesas = obtener_mesas(lobby)
        texto = leerTexto(mesas)
        mesas_libres = buscar_mesa(texto)
        posicion_x, posicion_y = localizacion_mesas(mesas_libres, mesas, posicion_mesas, posicion_lobby)
        activarBotonMesa(posicion_x, posicion_y)
        posicion_registro = buscar_registrar(lobby, posicion_lobby)
        activarBotonRegistro(posicion_registro)
        sleep(1)
        pantalla = capturarPantalla()
        lobby, posicion_lobby = obtener_lobby(pantalla)
        posicion_registro_final = buscar_registrar_final(lobby, posicion_lobby)
        activarBotonRegistro(posicion_registro_final)
    except:
        registrar = False
        print("No se ha podido registrar")
    
    return registrar
    """
    for linea in texto:
        print(linea)
    
    print("\nLas mesas estaran en las líneas: ", mesas_libres)
    print(f"La localizacion del lobby ({posicion_lobby[0]}x{posicion_lobby[1]})")
    print(f"La localizacion de las mesas ({posicion_mesas[0]}x{posicion_mesas[1]})")
    print(f"La localizacion del puntero sera ({posicion_x}x{posicion_y})")
    print(f"El boton de registro se encuentra en ({registro_x}x{registro_y})")
    
    cv2.imwrite("./images/lobby.png", lobby)
    cv2.imwrite("./images/mesas.png", mesas)
    cv2.imwrite("./images/real.png", pantalla)
    """

def capturarPantalla():
    img = pyautogui.screenshot()
    try:
        img_np = np.array(img)
    except MemoryError:
        print("Error en memoria")   
    pantalla = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return pantalla

def main():
    path = "C:/Users/Usuario/Desktop/Registro-Automatico/images/real.png"
    imagen = cv2.imread(path)
    pantalla = capturarPantalla()
    lobby, posicion_lobby = obtener_lobby(imagen)
    mesas, posicion_mesas = obtener_mesas(lobby)
    texto = leerTexto(mesas)
    mesas_libres = buscar_mesa(texto)
    posicion_x, posicion_y = localizacion_mesas(mesas_libres, mesas,  posicion_mesas, posicion_lobby)
    escribir_localizacion(posicion_x, posicion_y)
    posicion_registro = buscar_registrar(lobby, posicion_lobby)
    x, y, w, h = posicion_registro["registro"]
    print(x, y, w, h)
    
    path = "C:/Users/Usuario/Desktop/Registro-Automatico/images/prueba2.png"
    imagen = cv2.imread(path)
    lobby_registro, posicion_lobby = obtener_lobby(imagen)
    posicion_registro_final = buscar_registrar_final(lobby_registro, posicion_lobby)
    pantalla = capturarPantalla()
    ## imprimo resultados
    for linea in texto:
        print(linea)
    print("\nLas mesas estaran en las líneas: ", mesas_libres)
    print(f"La localizacion del lobby ({posicion_lobby[0]}x{posicion_lobby[1]})")
    print(f"La localizacion de las mesas ({posicion_mesas[0]}x{posicion_mesas[1]})")
    print(f"La localizacion del puntero sera ({posicion_x}x{posicion_y})")
    print(f"El boton de registro se encuentra en {posicion_registro}")
    print(f"El boton de registro final se encuentra en {posicion_registro_final}")
    cv2.imwrite("./images/lobby.png", lobby)
    cv2.imwrite("./images/mesas.png", mesas)
    cv2.imwrite("./images/lobby_registro.png", lobby_registro)
    #mostrarImagen(mesas)
    #mostrarImagen(pantalla)
    

if __name__ == '__main__':
    sleep(3)
    registrarSit()
    #main()
    
    
    


