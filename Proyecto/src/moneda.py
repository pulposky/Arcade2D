# src/moneda.py
# Define la clase Moneda y su comportamiento dentro del juego de plataformas.

import pygame
from settings import *
import random

class Moneda(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        # Cuerpo visual de la moneda: un círculo amarillo.
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (15, 15), 15)  # Dibuja un círculo amarillo
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, jugador):
        # Si el jugador colisiona con la moneda...
        if self.rect.colliderect(jugador.rect):
            print("¡Moneda recogida!")  # Imprime el puntaje actualizado en la consola
            
            # ...la moneda se mueve a otra posición aleatoria dentro de la ventana
            self.rect.center = (
                random.randint(50, ANCHO - 50),
                random.randint(50, ALTO - 50)
            )
            return 1  # Indica que se recogió la moneda
        return 0  # No se recogió la moneda
    
    def dibujar(self, ventana):
        # Método para dibujar la moneda en la ventana del juego.
        ventana.blit(self.image, self.rect)
        
    def resetear(self, x, y, grupo=None):
        # Cambia la posición de la moneda a (x, y)
        self.rect.center = (x, y)
        # Si se pasa un grupo, agrega la moneda de nuevo al grupo para que se dibuje
        if grupo is not None:
            grupo.add(self)