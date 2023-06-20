import pygame
pantalla = pygame.display.set_mode((1000, 500))

class Auto:
    def __init__(self, imagen, velocidad, intervalo, escala, tiempo, lugar):
            self.imagen = pygame.image.load(imagen)
            self.imagen = pygame.transform.scale(self.imagen, escala)
            self.imagen = pygame.transform.rotate(self.imagen, -180)
            self.velocidad = velocidad
            self.intervalo = intervalo / 1000
            self.escala = escala
            self.tiempo = tiempo
            self.lugar = lugar
            self.rect = self.imagen.get_rect()
            self.rect.x = -800
