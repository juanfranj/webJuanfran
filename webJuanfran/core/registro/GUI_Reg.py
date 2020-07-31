from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from libs.Funciones_GUI import *


if __name__ == '__main__':
	 
	root = Tk()
	root.geometry("+1708+930")

	#---------------------------------Variables-------------------------------------
	bot = BooleanVar()
	bot.set(1)

	# --------------------------------Título----------------------------------------
	root.iconbitmap("./images/logo.ico")
	root.title("App_Regs")
	# ---------------------------------Barra de Menu--------------------------------
	barraMenu = Menu(root)
	root.config(menu = barraMenu, width = 300, height = 300)

	archivoMenu=Menu(barraMenu, tearoff = 0)
	barraMenu.add_cascade(label="Inicio", menu=archivoMenu)

	archivoMenu.add_command(label = "Start", command = lambda:inicioRegistro(bot.get) )
	archivoMenu.add_command(label = "Stop", command = lambda:finRegistro(root) )
	archivoMenu.add_separator()
	archivoMenu.add_command(label = "Salir", command = lambda:salirAplicacion(root))
	# ------------------------------------------------------------------------------
	# ------------------------------- Frames----------------------------------------
	# --------------------------------Botones---------------------------------------
	miFrame = Frame(root)
	miFrame.grid(row = 1, column = 0, columnspan = 2)
	#miFrame.config(bd = 2)
	miFrame.config(relief = "groove")
	#----------------------------------ChecBox--------------------------------------
	miFrame1 = Frame(root)
	miFrame1.grid(row = 2, column = 0, columnspan = 2)
	#miFrame1.config(bd = 2)
	#miFrame1.config(relief = "groove")
	#-------------------------------------------------------------------------------

	#----------------------------------Botonones-------------------------------------
	botonStart=Button(miFrame, text = "Start", command = lambda:inicioRegistro(bot.get))
	botonStart.grid(row = 1,column = 0,columnspan = 1, pady = 2)
	botonStart.config(width = 15)
	botonStart.config(cursor = "hand2")

	botonStop=Button(miFrame, text = "Stop", command = lambda:finRegistro(root))
	botonStop.grid(row = 1,column = 1,columnspan = 1, pady = 2)
	botonStop.config(width = 15)
	botonStop.config(cursor = "hand2")
	# ------------------------------------------------------------------------------
	#---------------------------------CheckBoton------------------------------------
	Label(miFrame1, text="Registro:      ").grid(row = 0, column = 0, sticky = "w", 
		columnspan = 1, pady = 5, padx=0)
	Radiobutton(miFrame1, text = "On", variable = bot, value = 1,
		command = vacio).grid(row = 0,column = 1, sticky = "e", padx=5)
	Radiobutton(miFrame1, text = "Off",variable = bot, value=0,
		command = vacio).grid(row = 0,column = 2, sticky = "e", padx=5)
	# ---------------------------------Fin GUI--------------------------------------

	root.mainloop()