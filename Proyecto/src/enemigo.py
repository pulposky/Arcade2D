# src/enemigo.py
import pygame
import random
from settings import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(ROJO)
        self.velocidad = 2
        self.vel_max   = 3

        # Aparecer en un borde aleatorio
        borde = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        if borde == "arriba":
            x = random.randint(0, ANCHO)
            y = -25
        elif borde == "abajo":
            x = random.randint(0, ANCHO)
            y = ALTO + 25
        elif borde == "izquierda":
            x = -25
            y = random.randint(0, ALTO)
        else:
            x = ANCHO + 25
            y = random.randint(0, ALTO)

        self.rect = self.image.get_rect(center=(x, y))

    def aumentar_velocidad(self):
        if self.velocidad < self.vel_max:
            self.velocidad = min(self.velocidad + 0.5, self.vel_max)

    def update(self, jugador):
        # Moverse en línea recta hacia el jugador
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        distancia = max(1, (dx**2 + dy**2) ** 0.5)  # evitar división por 0

        self.rect.x += int(self.velocidad * dx / distancia)
        self.rect.y += int(self.velocidad * dy / distancia)