import pygame
from pygame.locals import *
import random
from class_autos import *
from ranking import mostrar_ranking
import sqlite3
from colores import *
from pygame import mixer

pygame.init()
mixer.init()
#---------------------------------------------------------------------------------------------------------------
# Seteo el largo y ancho de la ventana
pantalla = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Carrera")
#Agrego a la pantalla principal el fondo y lo bliteo
fondo_juego = pygame.image.load("ruta1.png").convert()
fondo_juego = pygame.transform.scale(fondo_juego, (1000, 500))
pantalla.blit(fondo_juego, (0, 0))

#Defino las imagenes de los botones 
imagen_jugar = pygame.image.load("boton_jugar.png")
imagen_jugar = pygame.transform.scale(imagen_jugar,(200, 100))
imagen_resume = pygame.image.load("boton_resume.png")
imagen_resume = pygame.transform.scale(imagen_resume, (200, 100))
rect_boton = imagen_jugar.get_rect()
rect_boton.y = 400
rect_boton.x = 600

imagen_ranking = pygame.image.load("boton_ranking.png")
imagen_ranking = pygame.transform.scale(imagen_ranking,(200, 100))
rect_boton_puntos = imagen_ranking.get_rect()
rect_boton_puntos.y = 200
rect_boton_puntos.x = 600

#Agrego los efectos de sonido
audio_fondo = pygame.mixer.Sound("audio_ruta.mp3")
audio_fondo.set_volume(0.05)
audio_mancha = pygame.mixer.Sound("audio_mancha.mp3")
audio_choque = pygame.mixer.Sound("audio_choque.mp3")

#---------------------------------------------------------------------------------------------------------------
#Instancio cada uno de los autos
auto_principal = Auto("auto_principal.png", 3, 0, (110, 100), 0, None)
auto_principal.rect.x = 100
auto_principal.rect.y = 50
auto_chocado = Auto("auto_chocado.png", 0, 0, (150, 150), 0, None)
mancha = Auto("auto_mancha.png", 3, 9700, (80, 100), 0, "arriba")
#Instancio todos los autos que se van a ir generando
autos_generados = [
    Auto("auto_policia.png", 6, 900, (100, 120), 0, "abajo"),
    Auto("auto_ambulancia.png", 4, 1100, (140, 120), 0, "abajo"),
    Auto("auto_taxi.png", 3, 1000, (120, 100), 0, "arriba"),
    Auto("auto_bondi.png", 3, 1400, (150, 250), 0, "arriba"),
    Auto("auto_policia.png", 6, 1400, (100, 120), 0, "abajo"),
    Auto("auto_ambulancia.png", 4, 2700, (140, 120), 0, "abajo"),
    Auto("auto_taxi.png", 3, 1700, (120, 100), 0, "arriba"),
    Auto("auto_bondi.png", 3, 2100, (150, 250), 0, "arriba")
]

#---------------------------------------------------------------------------------------------------------------
#Bandera de inicio del juego
flag_game = True
#Variable que define en que parte del menu empieza el juego
opcion = 0
#Bandera que define el estado de la partida
game_over = False
#Bandera que define si ya se ingreso el puntaje
flag_ranking = True


#---------------------------------------------------------------------------------------------------------------
#Variables que utilizo para la creacion del input del nombre del usuario
nombre_ingresado = ''
input_rect = pygame.Rect(700, 400, 200, 50)
color_no = BLACK
color_si = LIGHTBLUE3
color = color_no
flag_texto = False
fuente_nombre = pygame.font.Font(None, 36)

#---------------------------------------------------------------------------------------------------------------
#Creo el rectángulo del contador de segundos y rectángulo del velocímetro
fuente_contador = pygame.font.Font(None, 36)
contador_rect = pygame.Rect(pantalla.get_width() - 150, 10, 140, 40)
fuente_velocimetro = pygame.font.Font(None, 36)
velocimetro_rect = pygame.Rect(0, 20, 10, 140)

#---------------------------------------------------------------------------------------------------------------
# Creo el programa principal
while flag_game:
    #La opxion 0 es el menu principal
    if opcion == 0:
        pantalla.blit(fondo_juego, (0, 0))
        #Posiciono boton start
        start_x = 400
        start_y = 100 
        rect_boton.topleft = (start_x, start_y)
        pantalla.blit(imagen_jugar, rect_boton)
        #Posiciono boton ranking
        ranking_x = 400 
        ranking_y = 300
        rect_boton_puntos.topleft = (ranking_x, ranking_y)
        #Los muestro en pantalla
        pantalla.blit(imagen_ranking, rect_boton_puntos)

        #Dibujo el rectangulo del input del nombre del usuario
        pygame.draw.rect(pantalla, color, input_rect, 2)
        texto = fuente_nombre.render(nombre_ingresado, True, (255, 255, 255))
        pantalla.blit(texto, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, texto.get_width() + 10)
        pygame.display.flip()

        for evento in pygame.event.get():
            #Si el usuario quiere cerrar, puede
            if evento.type == pygame.QUIT:
                flag_game = False

            #Si el usuario presiona para escribir su nombre 
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(evento.pos):
                    flag_texto = True
                else:
                    flag_texto = False

                #Si el usuario presiona para jugaro ver el ranking
                if rect_boton.collidepoint(pygame.mouse.get_pos()):
                    pantalla.blit(fondo_juego, (0, 0))
                    tiempo_inicial = pygame.time.get_ticks()
                    opcion = 1
                elif rect_boton_puntos.collidepoint(pygame.mouse.get_pos()):
                    opcion = 2

            #Solo puede escribir su nombre si presiona
            if evento.type == pygame.KEYDOWN:
                if flag_texto == True:
                    if evento.key == pygame.K_BACKSPACE:
                        nombre_ingresado = nombre_ingresado[:-1]
                    else:             
                        nombre_ingresado += evento.unicode

        #Cambia el color del input dependiendo de si esta presionado o no
        if flag_texto:
            color = color_si
        else:
            color = color_no

#---------------------------------------------------------------------------------------------------------------
    #La opcion 2 es el ranking
    elif opcion == 2:
        #Dibujo en pantalla el boton del menu, y muestro el ranking
        pantalla.blit(fondo_juego, (0, 0))
        fuente_main_menu = pygame.font.Font(None, 32)
        texto_main_menu = fuente_main_menu.render("Main Menu", True, (0, 0, 0))
        rect_main_menu = texto_main_menu.get_rect(center=(800, 200))
        #Fondo blanco de boton main menu
        pygame.draw.rect(pantalla, (225, 225, 255), rect_main_menu, border_radius=8)
        pantalla.blit(texto_main_menu, rect_main_menu)
        mostrar_ranking(pantalla)
        pygame.display.flip()

        for evento in pygame.event.get():
            #Si el usuario quiere cerrar, puede
            if evento.type == pygame.QUIT:
                    flag_game = False
            #Si el usuario toca el boton del menu, vuelve alli
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_main_menu.collidepoint(pygame.mouse.get_pos()):
                    opcion = 0

#---------------------------------------------------------------------------------------------------------------
    #La opcion 1 es el bucle principal del juego
    elif opcion == 1:
        #Si el usuario quiere cerrar, puede
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                flag_game = False
        #Usa la funcion de locals que detecta el presionamiento de teclas
        keys = pygame.key.get_pressed()
        # Mientras no se haya perdido
        if not game_over:
            flag_ranking = True
            #Sonido de fondo
            audio_fondo.play()
            #Movimiento del auto con las teclas de flechitas, ajusta la posicion con tal velocidad
            if keys[K_LEFT] and auto_principal.rect.left > 0:
                auto_principal.rect.x -= auto_principal.velocidad
            if keys[K_RIGHT] and auto_principal.rect.right < pantalla.get_width():
                auto_principal.rect.x += auto_principal.velocidad
            if keys[K_UP] and auto_principal.rect.top > 0:
                auto_principal.rect.y -= auto_principal.velocidad
            if keys[K_DOWN] and auto_principal.rect.bottom < pantalla.get_height():
                auto_principal.rect.y += auto_principal.velocidad

            #Muestra en pantalla los elementos de la superficie
            pantalla.blit(fondo_juego, (0, 0))
            pantalla.blit(mancha.imagen, mancha.rect)
            pantalla.blit(auto_principal.imagen, auto_principal.rect)

            #Empieza a tomar el tiempo 
            tiempo_actual = pygame.time.get_ticks()

            #Pasa de milisegundos a segundos
            segundos_transcurridos = (tiempo_actual - tiempo_inicial) // 1000
            #Creo la lista vacia para ir guardando cada auto que ya pasó
            autos_actualizados = []
            #Itero la lista de autos a generarse y si ya salio de la pantalla y paso su intervalo, genero otro 
            for auto in autos_generados:
                if auto.rect.left <= -300 and segundos_transcurridos - auto.tiempo >= auto.intervalo:
                    auto.tiempo = segundos_transcurridos
                    #Dependiendo del lugar donde debe generarse, aparece ahi
                    if auto.lugar == "arriba":
                        auto.rect.center = (pantalla.get_width(), random.randint(0, pantalla.get_height() // 2))
                    else:
                        auto.rect.center = (pantalla.get_width(), random.randint(pantalla.get_height() // 2, pantalla.get_height()))
                #Mueve el auto a la izquierda por su respectiva velocidad
                auto.rect.x -= auto.velocidad
                #Saco la mascara de la superficie de cada auto y calculo su posicion con respecto al principal
                auto_mask = pygame.mask.from_surface(auto.imagen)
                auto_principal_mask = pygame.mask.from_surface(auto_principal.imagen)
                posiciones = (auto.rect.x - auto_principal.rect.x, auto.rect.y - auto_principal.rect.y)
                #Usando la funcion overlap de las mascaras, busco si hay alguna colision
                if auto_principal_mask.overlap(auto_mask, posiciones):
                    #Si hay colisiones, saco el sonido de fondo y reproduzco el efecto de choque 
                    audio_fondo.stop()
                    audio_choque.play()
                    #Game over = true abre el mini menu post patida
                    game_over = True
                    #Cambio la imagen del auto que se choco
                    auto.imagen = auto_chocado.imagen
                pantalla.blit(auto.imagen, auto.rect)
                #Guardo los autos que pasaron en esta lista asi no se traba el juego
                autos_actualizados.append(auto)

            #Hago lo mismo pero para la mancha de aceite 
            if mancha.rect.left <= -300 and segundos_transcurridos - mancha.tiempo >= mancha.intervalo:
                mancha.tiempo = segundos_transcurridos
                mancha.rect.center = (pantalla.get_width(), random.randint(0, pantalla.get_height() // 2))
            mancha.rect.x -= mancha.velocidad
            mancha_mask = pygame.mask.from_surface(mancha.imagen)
            auto_principal_mask = pygame.mask.from_surface(auto_principal.imagen)
            posiciones_man = (mancha.rect.x - auto_principal.rect.x, mancha.rect.y - auto_principal.rect.y)
            if auto_principal_mask.overlap(mancha_mask, posiciones_man):
                game_over = False
                auto_principal.velocidad = random.randint(1, 6)
                audio_mancha.play()

            #Si el tiempo excede los 20 segundos, los autos se vuelven mas rapido
            if segundos_transcurridos > 20:
                for auto in autos_generados:
                    if auto.lugar == "arriba":
                        auto.velocidad = 4
                    else:
                        auto.velocidad = 7

            #Muestro los rects de tiempo y velocidad
            texto_contador = fuente_contador.render(f"Tiempo: {segundos_transcurridos} s", True, (255, 255, 255))
            pantalla.blit(texto_contador, contador_rect)
            texto_velocimetro = fuente_velocimetro.render(f"Velocidad: {auto_principal.velocidad}", True, (255, 255, 255))
            pantalla.blit(texto_velocimetro, velocimetro_rect)

        #Si se perdió
        else:
            if flag_ranking == True:
                #Utilizando la base de datos SQL creo la tabla de los rankings
                with sqlite3.connect("ranking.db") as conexion:
                    try:
                        #Si no existe la tabla la crea
                        sentencia = '''CREATE TABLE IF NOT EXISTS ranking
                            (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT,
                            tiempo INTEGER
                            )
                            '''
                        conexion.execute(sentencia)
                        print("Se creó la tabla ranking")
                    except sqlite3.OperationalError:
                        print("La tabla ranking ya existe")

                    try:
                        #Guarda en la tabla el nombre del usuario y su puntaje
                        conexion.execute("INSERT INTO ranking (nombre, tiempo) VALUES (?, ?)", (nombre_ingresado, segundos_transcurridos))
                        conexion.commit()
                        print("Registro insertado correctamente")
                    except:
                        print("Error al insertar el registro")
                    flag_ranking = False

            if evento.type == pygame.QUIT:
                flag_game = False
            #Muestro cartel de Game Over
            fuente = pygame.font.Font(None, 64)
            texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
            pantalla.blit(texto_game_over, (350, 200))

            # Muestro opción "Try Again"
            fuente_try_again = pygame.font.Font(None, 32)
            texto_try_again = fuente_try_again.render("Try Again", True, (0, 0, 0))
            rect_try_again = texto_try_again.get_rect(center=(500, 300))
            pygame.draw.rect(pantalla, (225, 225, 255), rect_try_again, border_radius=8)
            pantalla.blit(texto_try_again, rect_try_again)

            #Muestro cartel menu principal
            fuente_main_menu = pygame.font.Font(None, 32)
            texto_main_menu = fuente_main_menu.render("Main Menu", True, (0, 0, 0))
            rect_main_menu = texto_main_menu.get_rect(center=(500, 400))
            pygame.draw.rect(pantalla, (225, 225, 255), rect_main_menu, border_radius=8)
            pantalla.blit(texto_main_menu, rect_main_menu)

            #Depende que presione el usuario, juega de nuevo o vuelve al menu
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN):
                    if rect_main_menu.collidepoint(pygame.mouse.get_pos()):
                        imagen_jugar = imagen_resume
                        opcion = 0
                        pantalla.blit(fondo_juego, (0, 0))
                    elif rect_try_again.collidepoint(pygame.mouse.get_pos()):
                        #Reinicio el juego estableciendo los valores de todo al inicial
                        game_over = False
                        tiempo_inicial = pygame.time.get_ticks()
                        auto_principal.rect.x = 100
                        auto_principal.rect.y = 50
                        auto_principal.velocidad = 3
                        mancha = Auto("auto_mancha.png", 3, 9700, (80, 100), 0, "arriba")
                        autos_generados = [
                            Auto("auto_policia.png", 6, 900, (100, 120), 0, "abajo"),
                            Auto("auto_ambulancia.png", 4, 1100, (140, 120), 0, "abajo"),
                            Auto("auto_taxi.png", 3, 1000, (120, 100), 0, "arriba"),
                            Auto("auto_bondi.png", 3, 1400, (150, 250), 0, "arriba"),
                            Auto("auto_policia.png", 6, 1500, (100, 120), 0, "abajo"),
                            Auto("auto_ambulancia.png", 4, 2700, (140, 120), 0, "abajo"),
                            Auto("auto_taxi.png", 3, 1700, (120, 100), 0, "arriba"),
                            Auto("auto_bondi.png", 3, 2100, (150, 250), 0, "arriba")
                        ]
        pygame.display.flip()
pygame.quit()
