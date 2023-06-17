import sqlite3
import pygame
import colores

def mostrar_ranking(pantalla):
    # Establecer conexión a la base de datos
    conexion = sqlite3.connect("ranking.db")
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para obtener los datos del ranking
    cursor.execute("SELECT nombre, tiempo FROM ranking ORDER BY tiempo DESC LIMIT 5")
    resultados = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conexion.close()

    # Obtener dimensiones de la pantalla
    pantalla_ancho, pantalla_alto = pantalla.get_size()

    # Calcular posición vertical inicial para el primer ranking
    posicion_y = (pantalla_alto - (50 * len(resultados))) // 2

    # Iterar sobre los resultados de la consulta SQL
    for i, resultado in enumerate(resultados):
        nombre = resultado[0]
        tiempo = resultado[1]

        # Calcular posición horizontal para el texto del ranking
        posicion_x = (pantalla_ancho - 200) // 2

        font_nombre = pygame.font.SysFont("Arial", 24)
        texto_nombre = font_nombre.render(nombre, True, colores.GREEN2)

        # Calcular posición vertical para el texto del ranking
        texto_y = posicion_y + (i * 50)

        pantalla.blit(texto_nombre, (posicion_x, texto_y))

        font_tiempo = pygame.font.SysFont("Arial", 24)
        texto_tiempo = font_tiempo.render(str(tiempo), True, colores.GREEN2)
        pantalla.blit(texto_tiempo, (posicion_x + 150, texto_y))

    pygame.display.flip()
