import sqlite3
import pygame
import colores

def mostrar_ranking(pantalla):
    #Conecto a la base de datos
    conexion = sqlite3.connect("ranking.db")
    cursor = conexion.cursor()

    #Obtengo los datos del juego
    cursor.execute("SELECT nombre, tiempo FROM ranking ORDER BY tiempo DESC LIMIT 5")
    resultados = cursor.fetchall()

    #Cierro la conexion a la base de datos
    conexion.close()

    #Posicion puntajes
    posicion_y = 150

    #Itero para cada resultado dando los valores
    for i, resultado in enumerate(resultados):
        nombre = resultado[0]
        tiempo = resultado[1]

        posicion_x = 400

        fuente_nombre = pygame.font.SysFont("Arial", 24)
        texto_nombre = fuente_nombre.render(nombre, True, colores.GREEN2)

        #Pongo cada nombre con su puntaje
        texto_y = posicion_y + (i * 50)

        pantalla.blit(texto_nombre, (posicion_x, texto_y))

        font_tiempo = pygame.font.SysFont("Arial", 24)
        texto_tiempo = font_tiempo.render(str(tiempo), True, colores.GREEN2)
        pantalla.blit(texto_tiempo, (posicion_x + 150, texto_y))

    pygame.display.flip()
