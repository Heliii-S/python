#PARA HACER LA VENTANA INICIAL
import tkinter as tk
v = tk.Tk()
v.title("JUEGO DE MEMORIA")
v.geometry("900x700")
v.resizable(False,False)

#PARA MOSTRAR DIFERENTES FRAME SEGÚN EL BOTÓN QUE PRESIONO
def mostrar_frame(nombre):
    menu.pack_forget()
    Fácil.pack_forget()
    Normal.pack_forget()
    Medio.pack_forget()
    Difícil.pack_forget()
    if nombre == "menu":
        menu.pack()
    elif nombre == "Fácil":
        Fácil.pack()
    elif nombre == "Normal":
        Normal.pack()
    elif nombre == "Medio":
        Medio.pack()
    elif nombre == "Difícil":
        Difícil.pack()

#PARA MOSTRAR UN TABLERO DIFERENTE SEGÚN EL NIVEL
"""""
def tablero(nombre):
    if nombre == "Fácil":
        for i in range(1,3):
    elif nombre == "Normal":
        Normal.pack()
    elif nombre == "Medio":
        Medio.pack()
    elif nombre == "Difícil":
        Difícil.pack()
"""

#PARA MOSTRAR EL MENÚ
menu = tk.Frame(v)
texto1 = tk.Label(menu,text="Elige el nivel \nque quieres jugar: ",font=("Arial",64))
b1 = tk.Button(menu,text="Fácil",font=("Arial",54),command=lambda: mostrar_frame("Fácil"))
b2 = tk.Button(menu,text="Normal",font=("Arial",54),command=lambda: mostrar_frame("Normal"))
b3 = tk.Button(menu,text="Medio",font=("Arial",54),command=lambda: mostrar_frame("Medio"))
b4 = tk.Button(menu,text="Difícil",font=("Arial",54),command=lambda: mostrar_frame("Difícil"))

texto1.pack()
b1.pack()
b2.pack()
b3.pack()
b4.pack()

#FRAMES POR NIVEL
Fácil = tk.Frame(v)
b5 = tk.Button(Fácil,text="Volver", font=("Arial",54), command = lambda: mostrar_frame("menu"))
Normal = tk.Frame(v)
b6 = tk.Button(Normal,text="Volver", font=("Arial",54), command = lambda: mostrar_frame("menu"))
Medio = tk.Frame(v)
b7 = tk.Button(Medio,text="Volver", font=("Arial",54), command = lambda: mostrar_frame("menu"))
Difícil = tk.Frame(v)
b8 = tk.Button(Difícil,text="Volver", font=("Arial",54), command = lambda: mostrar_frame("menu"))

mostrar_frame("menu")
v.mainloop()