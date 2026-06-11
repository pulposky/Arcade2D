# src/moneda.py
import pygame
import random
import os
from settings import *

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))

        base = os.path.dirname(os.path.abspath(__file__))
        ruta_sonido = os.path.join(base, "..", "assets", "sounds", "recogerMoneda.mp3")
        self.sonido_moneda = pygame.mixer.Sound(ruta_sonido)
        self.sonido_moneda.set_volume(0.3)

    def update(self, jugador):
        if self.rect.colliderect(jugador.rect):
            self.sonido_moneda.play()
            # La reposición ahora la maneja main.py con posicion_libre()
            return 1
        return 0
