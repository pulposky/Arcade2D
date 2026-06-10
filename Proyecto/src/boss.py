import math
import time

import pygame

from settings import ANCHO, MORADO, ROJO
from src.rayo import Rayo


class Boss(pygame.sprite.Sprite):
    def __init__(self, mundo_ancho, dificultad=1):
        super().__init__()
        self.image = pygame.Surface((90, 90))
        self.image.fill(MORADO)
        self.rect = self.image.get_rect(midtop=(mundo_ancho // 2, 40))
        self.vida_max = 12 + dificultad * 6
        self.vida = self.vida_max
        self.velocidad = 2 + dificultad * 0.2
        self.intervalo_disparo = max(0.8, 2.2 - dificultad * 0.15)
        self.ultimo_disparo = time.time()
        self.direccion = 1

    def update(self, mundo_ancho, jugador, rayos):
        self.rect.x += int(self.velocidad * self.direccion)
        if self.rect.left <= 0 or self.rect.right >= mundo_ancho:
            self.direccion *= -1

        ahora = time.time()
        if ahora - self.ultimo_disparo >= self.intervalo_disparo:
            self.disparar(jugador, rayos)
            self.ultimo_disparo = ahora

    def disparar(self, jugador, rayos):
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        distancia = max(1, math.sqrt(dx * dx + dy * dy))
        rayo = Rayo(
            self.rect.centerx,
            self.rect.bottom,
            (dx / distancia, dy / distancia),
        )
        rayos.add(rayo)

    def recibir_dano(self, cantidad):
        self.vida = max(0, self.vida - cantidad)
        return self.vida <= 0

    def dibujar_barra_vida(self, superficie, camara_x):
        ancho = 180
        alto = 14
        x = self.rect.centerx - camara_x - ancho // 2
        y = self.rect.top - 24
        porcentaje = self.vida / self.vida_max

        pygame.draw.rect(superficie, ROJO, (x, y, ancho, alto))
        pygame.draw.rect(superficie, (40, 220, 80), (x, y, int(ancho * porcentaje), alto))
        pygame.draw.rect(superficie, (255, 255, 255), (x, y, ancho, alto), 2)
