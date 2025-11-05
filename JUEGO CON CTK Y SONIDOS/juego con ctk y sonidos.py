#IMPORTS QUE VOY A OCUPAR
import random
import customtkinter as ctk
import tkinter as tk
import pygame #para agregar efectos de sonido y música
import os #para que acceda a la carpeta de sonidos

base_path = os.path.dirname(os.path.abspath(__file__)) # es la ruta donde está mi juego
""" __file__ es el nombre del archivo de python que se ejecuta
os.path.abspath convierte el file en la ruta que se sigue.. va de mis usuarios, al usuario donde estoy, el escritorio e ingresa a mi carpeta
os.path.dirname() quita el nombre del archivo y deja solo la carpeta
base_path es la ruta exacta donde esta mi juego en mi computadora
"""
ruta_sonido_boton = os.path.join(base_path,"sonidos","botones.wav")
# os.path.join pone la ruta que se debe seguir para acceder al archivo escrita correctamente, con los // que lleve, etc.
ruta_sonido_cubito = os.path.join(base_path,"sonidos","cubitos.wav")
# en todas estas rutas, base_path es la carpeta del juego, "sonidos" es la subcarpeta y "" son los archivos a los que se va a acceder dentro de la carpeta sonidos
ruta_sonido_derrota = os.path.join(base_path,"sonidos","mal.wav")
ruta_sonido_victoria = os.path.join(base_path,"sonidos","bien.wav")
ruta_musica_fondo = os.path.join(base_path,"sonidos","musicafondo.wav")
#para sonidos y música
pygame.mixer.init()
sonido_boton = pygame.mixer.Sound(ruta_sonido_boton)
sonido_cubito = pygame.mixer.Sound(ruta_sonido_cubito)
sonido_victoria = pygame.mixer.Sound(ruta_sonido_victoria)
sonido_derrota = pygame.mixer.Sound(ruta_sonido_derrota)
pygame.mixer.music.load(ruta_musica_fondo)
pygame.mixer.music.play(-1) #para repetir infinitamente
pygame.mixer.music.set_volume(0.5)

#DECLARACIÓN DE LISTAS DONDE SE VAN A IR GUARDANDO LOS DATOS
cuadrados = []
lista_bot = [] #PARA GUARDAR EL PATRÓN ORIGINAL
lista_usuario = [] #PARA GUARDAR EL PATRÓN QUE INGRESE EL JUGADORES
esperando_respuesta = False
niveles = 0 #AQUÍ SE VAN A IR GUARDANDO CUANTOS NIVELES HA GANADO EL JUGADOR
rondas = 0 #AQUÍ SE VAN A IR GUARDANDO CUANTAS RONDAS HA JUGADOR EL JUGADOR

#PARA HACER LA VENTANA
v = ctk.CTk()
v.title("👾 JUEGO DE MEMORIA 👾")
v.geometry("900x700")
v.resizable(False,False)
v.configure(fg_color="#FFF8FB")

tablero = tk.Canvas(v,width=500,height=500,highlightthickness=0) #highlightthickness elimina el borde por defecto del canvas
mensajes = tk.Frame(v,bg="#FFF8FB") #donde van los distintos mensajes a lo largo del juego para que sea más facil controlar que no se muestren en el menú al jugar varias veces
label = tk.Label(mensajes,text="",font=("Comic Sans MS",24), bg="#E7B7CC",fg="#7B6C8E")
label.pack()

#FUNCIÓN PARA MOSTRAR EL TIEMPO RESTANTE
def tiempo_restante(segundos):
    if segundos > 0:
        label.config(text=str(segundos))
        v.after(1000,tiempo_restante, segundos - 1) #USO AFTER PORQUE CON TIME SLEEP NO SE PUEDE
    else:
        label.config(text="¡Se acabó el tiempo! ⏰")

#DIBUJAR EL TABLERO QUE ES CORRECTO, en caso de que el jugador se equivoque para que vea que contestó mal
def pintar_correcto():
    global lista_bot, cuadrados
    sonido_boton.play()
    label.config(text="Este es el patrón correcto ✌️")
    for i in range(len(lista_bot)):
        color = lista_bot[i]
        cubito = cuadrados[i]
        tablero.itemconfig(cubito, fill=color) #para llenar el cuadrado que es con el color correcto
    b6.pack_forget()#olvidar el botón de ver la solución porque ya la estás viendo
    b7.pack(pady=10)
    b8.pack(pady=10)
    v.update() #mostrar cambios inmediatamente en pantalla

#FUNCIÓN PARA PODER CAMBIAR EL COLOR DE LOS CUADRADOS AL HACER CLICK
#SIGUIENDO EL ORDEN: AMARILLO -> AZUL -> ROJO
def cambio_colores(event):
    global esperando_respuesta
    if not esperando_respuesta:
        return #VA A IGNORAR SI HACER CLIC ANTES DE TIEMPO
    #esta función recibe el evento del clic
    cubito = event.widget.find_closest(event.x, event.y)[0]
    #esto es para encontrar la posición del cubo que se presiona y así saber a cual cambiarle el color, ya que hay varios
    #find_closest(), devuelve el pixel más cercano a x y a y.
    #[0] es solo para devolver el primer valor de la tupla, porque find_closest envía la respuesta como si fueran dos valores pero solo es uno
    color_actual = tablero.itemcget(cubito,"fill")
    #.itemcget(), obtiene cual es el relleno actual del "cubito" presionado
    if  color_actual == "LightGoldenrod1":
        nuevo_color = "SteelBlue2"
        sonido_cubito.play()
    elif color_actual == "SteelBlue2":
        nuevo_color = "IndianRed2"
        sonido_cubito.play()
    else:
        nuevo_color = "LightGoldenrod1"
        sonido_cubito.play()
    tablero.itemconfig(cubito,fill = nuevo_color)
    #el .itemconfig sirve para cambiar propiedades, en este caso cambia el color dependiendo de las condiciones del if-elif-else

#FUNCIÓN PARA CREAR LOS COLORES ALEATORIOS
def elegir_color(a):
    if a == 1:
        color = "LightGoldenrod1"
    elif a == 2:
        color = "SteelBlue2"
    elif a == 3:
        color = "IndianRed2"
    return color

#FUNCIÓN PARA LOS MENSAJES DE VICTORIA Y DE DERROTA ALEATORIOS, los mensajes fueron generados con CHATGPT
def elegir_mensaje(respuesta):
    m_victoria = [
    "🎉 ¡Impresionante memoria!",
    "🧠 ¡Recordaste todo a la perfección!",
    "💪 ¡Nada se te escapa, genio!",
    "✨ ¡Exacto! Tienes mente de acero.",
    "🔥 ¡Qué reflejos! Ni una falla.",
    "😎 ¡Eres una máquina de recordar!",
    "🎯 ¡Perfecto! Clavaste el patrón.",
    "🌟 ¡Excelente trabajo, campeón!",
    "🧩 ¡Todo en su lugar! ¡Bravo!",
    "🥇 ¡Ni un error! Vas por el récord.",
    "💥 ¡Asombroso! Tu concentración es increíble.",
    "🚀 ¡Velocidad y precisión!",
    "👏 ¡Así se hace! Nivel superado.",
    "🏆 ¡Memoria de elefante!",
    "🧘 ¡Concentración total, resultado perfecto!",
    "⚡ ¡Rápido y certero! ¡Muy bien!",
    "🌈 ¡Te lo sabes de memoria!",
    "🔓 ¡Nivel desbloqueado con maestría!",
    "💫 ¡Qué jugada tan limpia!",
    "🕹️ ¡Perfecto! Sigue así y romperás todos los récords.",
    "😏 ¡Vaya, parece que tienes neuronas extra!",
    "🧠 ¡Tu cerebro está en modo supercomputadora!",
    "🔥 ¡Lo lograste! No esperaba menos de ti… bueno, tal vez un poco menos.",
    "🎯 ¡Perfecto! ¿Seguro no tienes trucos ocultos?",
    "💪 ¡Wow! Ni Google recuerda tan bien.",
    "😎 ¡Imposible! O eres un genio o estás haciendo trampa.",
    "🎉 ¡Eso fue épico! El tablero se rinde ante ti.",
    "🚀 ¡Boom! Patrón destruido con precisión quirúrgica.",
    "🏆 ¡Excelente! Ya puedes presumirle a la IA.",
    "🤖 ¡Nivel humano superado! Bienvenido al club de los bots.",
    "🕶️ ¡Fácil, ¿no?! Vamos a ver si puedes repetirlo.",
    "✨ ¡Nada mal, mente brillante!",
    "🎮 ¡Combo perfecto! Tus reflejos son de videojuego.",
    "📀 ¡Grábate jugando esto, es arte!",
    "🧩 ¡Eres la pieza que faltaba!",
    "🍀 ¡Con suerte o sin ella, la rompiste!",
    "💥 ¡Tu memoria está encendida al máximo!",
    "⚡ ¡Rayos y centellas! ¡Qué velocidad!",
    "💫 ¡Brillante! Hasta los colores te aplauden.",
    "🎆 ¡Sigue así y dominarás el patrón universal!"
]
    m_derrota = ["😅 ¡Casi! Pero no era ese el patrón...",
    "💔 Uy, un pequeño error.",
    "🌀 ¡Te confundiste esta vez!",
    "⚠️ ¡Patrón incorrecto! Intenta de nuevo.",
    "🤔 Algo no cuadró ahí...",
    "😬 ¡Ay! Se mezclaron los colores.",
    "❌ No coincidió el patrón.",
    "💭 Parece que la memoria te jugó una broma.",
    "⏳ ¡Muy cerca! Pero fallaste en un detalle.",
    "🧊 Se te congeló la mente, ¿eh?",
    "😓 ¡Te equivocaste por poquito!",
    "🚫 No era ese orden. ¡Concéntrate!",
    "😵‍💫 Ups, se mezclaron las ideas.",
    "🫢 ¡Casi lo logras!",
    "🪞 La memoria te engañó esta vez.",
    "🔄 Error de patrón, inténtalo otra vez.",
    "💀 Fallo crítico... ¡pero puedes mejorar!",
    "🌧️ No pasa nada, cada error enseña algo.",
    "🪫 ¡Tu memoria se quedó sin batería!",
    "💢 ¡Ese no era el patrón correcto!",
    "🤖 El patrón te ganó... otra vez.",
    "😅 Tranquilo, nadie lo vio… bueno, casi nadie.",
    "🧠 Error 404: memoria no encontrada.",
    "💀 ¡Fallaste más rápido de lo que cargó el nivel!",
    "🎨 Esos colores no estaban ni cerca, artista.",
    "😬 ¡Wow! Eso fue... diferente.",
    "🫣 ¿Estabas jugando o meditando?",
    "🥴 Tu memoria se fue a dar una vuelta.",
    "💤 Despierta, el patrón no se repite solo.",
    "🫠 El tablero aún se está riendo.",
    "📉 ¡Eso dolió! Pero el siguiente será mejor, ¿no?",
    "🧊 ¡Frío, frío, frío!",
    "💥 ¡Explosión de errores detectada!",
    "🚫 No coincidió nada, pero se aprecia el esfuerzo.",
    "😵 ¡Tus colores hicieron freestyle!",
    "🪫 Tu memoria necesita recargarse urgentemente.",
    "🌪️ El caos del patrón te arrastró.",
    "📚 Estudia los colores la próxima vez 😏",
    "🫨 ¡Fallaste con estilo!",
    "🐢 No te preocupes, los grandes también se equivocan… a veces."
]
    if respuesta == 1:
        mensaje = random.choice(m_victoria)
    else:
        mensaje = random.choice(m_derrota)
    return mensaje
#FUNCIÓN PARA QUE LA COMPUTADORA "COMENTE" SOBRE TU DESEMPEÑO EN EL JUEGO, mensajes generados con CHATGPT
def mensaje_final(valor):
    m_felicitar = ["💪 ¡Eso fue casi perfecto! Tu memoria tiene músculos.",
    "🧠✨ ¡Casi un genio! Si el patrón tuviera emociones, estaría orgulloso.",
    "🔥 Tu memoria está en llamas (pero en el buen sentido).",
    "😎 ¡Excelente! Apenas fallaste… lo suficiente para parecer humano.",
    "👏 Wow, el patrón te respeta. Y eso no pasa seguido.",
    "🌟 ¡Brillante! Le diste una buena lección al azar.",
    "🤖 Tu memoria podría intimidar a una computadora vieja.",
    "📈 Si esto fuera un examen, tendrías un 9.9 (¡nada mal!).",
    "🔮 ¡Casi perfecto! Solo te faltó leerle la mente al juego.",
    "🎯 Eso estuvo tan bien que el patrón pidió una revancha.",
    "🧩 ¡Genial! Casi lograste engañar al propio algoritmo.",
    "🥇 Tu cerebro hoy merece una medalla (y una siesta).",
    "🤯 Ni los robots lo hacen tan bien, felicidades.",
    "☕ Tu memoria claramente tomó café antes de jugar.",
    "🧙‍♂️ ¡Buen trabajo! El patrón pensó que eras él.",
    "🔍 El juego tuvo que revisar dos veces, no podía creerlo.",
    "😱 Te acercaste tanto a la perfección que asusta un poco.",
    "👏 ¡Esa memoria merece aplausos de pie!",
    "😤 Parece que el patrón te tiene miedo ahora.",
    "🏆 Si sigues así, tendré que llamarte ‘El maestro de la memoria’."]

    m_derrota = ["😅 Wow... ¿intentaste adivinar con los ojos cerrados?",
    "🧠💨 Parece que la memoria no vino a jugar hoy.",
    "😂 Increíble... lograste fallar casi todas. ¡Eso también es un récord!",
    "🙃 No te preocupes, seguro la próxima vez fallas distinto.",
    "🚀 La NASA te llama… para estudiar cómo olvidaste tan rápido.",
    "🐟 ¡Asombroso! Lograste recordar menos que un pez dorado.",
    "🏖️ Tu cerebro pidió vacaciones, claramente.",
    "👀 Eso fue tan rápido que el patrón ni te conoció.",
    "🤝 Parece que el patrón y tú no se llevan muy bien.",
    "🧘‍♂️ Tranquilo, la memoria no lo es todo… solo en este juego.",
    "🏆 ¡Excelente! Si el objetivo era olvidar, ganaste.",
    "💔 El patrón te está demandando por abandono.",
    "🎨 No fue un fallo, fue una ‘reinterpretación creativa’ del patrón.",
    "🔋 Esa memoria está en modo ahorro de energía.",
    "😬 Por poco… pero no, nada que ver con el patrón.",
    "🚪 El patrón se fue, dijo que lo ignoraste demasiado.",
    "🤥 Podría decir que lo hiciste bien… pero estaría mintiendo.",
    "🌀 ¿Era un patrón o una ilusión óptica para ti?",
    "🎲 Parece que tu estrategia fue ‘no tener estrategia’.",
    "👏 Fallaste tanto que el patrón se despidió con aplausos lentos."]
    if valor == 1:
        mensaje = random.choice(m_felicitar)
    else:
        mensaje = random.choice(m_derrota)
    return mensaje
#FUNCIÓN PARA VERIFICAR LA RESPUESTA
def verificar():
    global lista_usuario, lista_bot, esperando_respuesta, niveles, rondas
    rondas += 1
    lista_usuario.clear()
    sonido_boton.play()
    for cuadrado in cuadrados:
        c = tablero.itemcget(cuadrado,"fill")
        lista_usuario.append(c)
    if lista_bot == lista_usuario:
        mensaje = elegir_mensaje(1)
        label.config(text=mensaje)
        sonido_victoria.play()
        b5.pack_forget()
        b7.pack(pady=10)
        b8.pack(pady=10)
        niveles += 1
    else:
       mensaje = elegir_mensaje(0)
       label.config(text=mensaje)
       sonido_derrota.play()
       b5.pack_forget()
       b6.pack(pady=10)
    esperando_respuesta = False
    

#FUNCION PARA VOLVER A PONER EL TABLERO AMARILLO LUEGO DEL TIEMPO, SEGÚN EL NIVEL
#DESPUÉS DE QUE todo VUELVE A SER AMARILLO, LLAMA A LA FUNCIÓN CAMBIAR COLOR PARA
#PERMITIR QUE EL USUARIO INGRESE EL NUEVO PATRÓN HACIENDO CLIC Y CAMBIANDO LOS COLORES
def amarillo():
    global esperando_respuesta, lista_bot, cuadrados
    esperando_respuesta = True
    for i in range(len(lista_bot)):
        cubito = cuadrados[i]
        tablero.itemconfig(cubito, fill="LightGoldenrod1") #para llenar cada cuadrado de amarillo
        tablero.tag_bind(cubito,"<Button-1>",cambio_colores)
        #con tag_bind se asocia un evento (hacer clic en este caso) con un objeto del canvas, el cuadrito
        #cubito es cada cuadrado que tiene el tablero según el nivel
        #el evento detecta que se presiona el cuadrado y llama a la función 
    #BOTÓN PARA SUBIR RESPUESTA
    b5.pack(pady=10)
    v.update() #para mostrar inmediatamente en pantalla


#FUNCIÓN DEL MENU QUE OCULTA LO DEMÁS Y MUESTRA LOS BOTONES DEL INICIO
def m_menu():
    v.configure(fg_color="#FFD1DC")
    menu.configure(bg="#FFD1DC")
    b7.pack_forget()
    b8.pack_forget()
    facil.pack_forget()
    normal.pack_forget()
    medio.pack_forget()
    dificil.pack_forget()
    tablero.pack_forget()
    mensajes.pack_forget()
    menu.pack()
    sonido_boton.play()
    v.update_idletasks() #refresca sin bloquear, sirve mejor que update() porque estoy haciendo muchas cosas

#FUNCION PARA MOSTRAR DIFERENTES FRAMES Y GENERAR LOS DISTINTOS TABLEROS SEGÚN EL NIVEL ELEGIDO
#MUESTRAN EL TABLERO INICIAL, HACEN LA CUENTA REGRESIVA Y LUEGO LLAMAN A LA FUNCIÓN PARA VOLVER todo AMARILLO
def tableropornivel(numero, tamaño_cubo, tiempo):
    global cuadrados, lista_bot
    cuadrados.clear()
    lista_bot.clear()
    tablero.delete("all")
    for i in range(numero): #número representa filas y columnas porque es el mismo número
        for j in range(numero):
            aleatorio = random.randint(1,3)
            r = tablero.create_rectangle(i*tamaño_cubo,j*tamaño_cubo,(i+1)*tamaño_cubo,(j+1)*tamaño_cubo, fill=elegir_color(aleatorio),outline="white")
            cuadrados.append(r)
            color = tablero.itemcget(r,"fill")
            lista_bot.append(color) #PARA GUARDAR LA SECUENCIA DE COLORES
    mensajes.pack()
    tablero.pack()
    v.update() #para actualizar y que se muestra a tiempo
    tiempo_restante(tiempo)
    tablero.after(tiempo*1000, amarillo) #se usa after porque con time sleep se pausa todo

#funciones para llamar a la funcion de tablero por nivel según el nivel, con los datos de cada uno
def n_facil():
    sonido_boton.play()
    v.configure(fg_color="#FFFACD")
    facil.configure(bg="#FFFACD")
    tablero.configure(bg="#FFFACD")
    label.configure(bg="#FFFACD")
    menu.pack_forget()
    facil.pack()
    tableropornivel(2,250,2)

def n_normal():
    sonido_boton.play()
    v.configure(fg_color="#CDEBFF")
    normal.configure(bg="#CDEBFF")
    tablero.configure(bg="#CDEBFF")
    label.configure(bg="#CDEBFF")
    menu.pack_forget()
    normal.pack()
    tableropornivel(3,160,3)

def n_medio():
    sonido_boton.play()
    v.configure(fg_color="#E2C2FF")
    medio.configure(bg="#E2C2FF")
    tablero.configure(bg="#E2C2FF")
    label.configure(bg="#E2C2FF")
    menu.pack_forget()
    medio.pack()
    tableropornivel(4,125,4)

def n_dificil():
    sonido_boton.play()
    v.configure(fg_color="#FFC0CB")
    dificil.configure(bg="#FFC0CB")
    tablero.configure(bg="#FFC0CB")
    label.configure(bg="#FFC0CB")
    menu.pack_forget()
    dificil.pack()
    tableropornivel(5,100,5)

#FUNCIÓN PARA MOSTRAR EL MENSAJE FINAL Y RESUMEN DEL JUEGO 
def m_salir():
    global niveles, rondas
    facil.pack_forget()
    normal.pack_forget()
    medio.pack_forget()
    dificil.pack_forget()
    tablero.pack_forget()
    menu.pack_forget()
    b7.pack_forget()
    b8.pack_forget()
    label.pack_forget()
    salir.pack()
    sonido_boton.play()
    texto2 = ctk.CTkLabel(salir,text="- RESUMEN DEL JUEGO -\n"f"Rondas que jugaste: {rondas} \nNiveles superados: {niveles}",font=("Comic Sans MS",30,"bold"),fg_color="#FFD1DC",text_color="#4A4A4A")
    texto2.pack()
    b9.pack(pady=10)
    if niveles < rondas:
        sonido_derrota.play()
        mensaje = mensaje_final(0)
        texto3 = tk.Label(text=mensaje, font=("Comic Sans MS",24),bg="#FFD1DC",fg="#4A4A4A")
        texto3.pack()
    else:
        sonido_victoria.play()
        mensaje = mensaje_final(1)
        texto4 = tk.Label(text=mensaje, font=("Comic Sans MS",24),bg="#FFD1DC",fg="#4A4A4A")
        texto4.pack()

#PARA CERRAR DEFINITIVAMENTE EL PROGRAMA CUANDO SE HACE CLICK EN EL BOTÓN
def salir_def():
    v.destroy()

#FRAME MENÚ Y SU CONTENIDO
menu = tk.Frame(v,bg="#FFD1DC")
texto1 = tk.Label(menu,text="Elige el nivel \nque quieres jugar: ",font=("Comic Sans MS",64,"bold"),bg="#FFD1DC",fg="#4A4A4A")
b1 = ctk.CTkButton(menu,text="Fácil 😴",font=("Comic Sans MS",36,"bold"),command=n_facil,fg_color="#FFFACD",text_color="#4A4A4A",hover_color="#FFFACD")
b2 = ctk.CTkButton(menu,text="Normal 😀",font=("Comic Sans MS",36,"bold"),command=n_normal,text_color="#4A4A4A",fg_color="#CDEBFF",hover_color="#CDEBFF")
b3 = ctk.CTkButton(menu,text="Medio ☺️",font=("Comic Sans MS",36,"bold"),command=n_medio,text_color="#4A4A4A",fg_color="#E2C2FF",hover_color="#E2C2FF")
b4 = ctk.CTkButton(menu,text="Exterminio 😵‍💫",font=("Comic Sans MS",36,"bold"),command=n_dificil,text_color="#4A4A4A",fg_color="#FFC0CB",hover_color="#FFC0CB")

#PARA QUE SE VEA EL TEXTO Y BOTONES
texto1.pack(pady=30)
b1.pack(pady=10)
b2.pack(pady=10)
b3.pack(pady=10)
b4.pack(pady=10)

#FRAMES DE NIVELES Y BOTONES
facil = tk.Frame(v,bg="#FFFACD")
normal = tk.Frame(v,bg="#CDEBFF")
medio = tk.Frame(v,bg="#E2C2FF")
dificil = tk.Frame(v,bg="#FFC0CB")
salir = tk.Frame(v,bg="#FFF8FB") #ESTE EL FRAME DONDE SE MOSTRARÁ EL PUNTAJE ANTES DE LA SALIDA DEFINITIVA

b5 = ctk.CTkButton(v,text="Enviar 💕",font=("Comic Sans MS",36,"bold"),command=verificar,text_color="#FFFFFF",fg_color="#de84c9",hover_color="#de84c9")
b6 = ctk.CTkButton(v,text="Oprime para ver la solución 💕",font=("Comic Sans MS",36,"bold"),command=pintar_correcto,text_color="#FFFFFF",fg_color="#de84c9",hover_color="#de84c9")
b7 = ctk.CTkButton(v,text="Volver a jugar 💕",font=("Comic Sans MS",36,"bold"),command=m_menu,text_color="#FFFFFF",fg_color="#de84c9",hover_color="#de84c9")
b8 = ctk.CTkButton(v,text="Salir",font=("Comic Sans MS",36,"bold"),command=m_salir,text_color="#FFFFFF",fg_color="#de84c9",hover_color="#de84c9")
b9 = ctk.CTkButton(v,text="Salir",font=("Comic Sans MS",36,"bold"),command=salir_def,text_color="#FFFFFF",fg_color="#de84c9",hover_color="#de84c9")

#PARA MOSTRAR EL MENÚ Y LA VENTANA
m_menu()
v.mainloop()