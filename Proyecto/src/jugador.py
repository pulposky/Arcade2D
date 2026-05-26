# src/jugador.py
# Define la clase Jugador y su comportamiento dentro del juego de plataformas.

import pygame
from settings import *

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cuerpo visual del jugador: un rectángulo azul.
        self.image = pygame.Surface((40, 60))
        self.image.fill(AZUL)
        # Rectángulo de colisión para posicionar y mover al jugador.
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        # Bandera que indica si el jugador está sobre una plataforma.
        self.en_suelo = False

    def update(self, plataformas):
        # Lógica de movimiento y manejo de colisiones cada frame.
        self.mover()
        self.aplicar_gravedad()

        # Mover horizontalmente y corregir colisiones.
        self.rect.x += self.vel_x
        self.colision_horizontal(plataformas)

        # Mover verticalmente y corregir colisiones.
        self.rect.y += self.vel_y
        self.colision_vertical(plataformas)

    def mover(self):
        # Leer el estado actual de las teclas.
        teclas = pygame.key.get_pressed()
        self.vel_x = 0
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))  # Limitar dentro de la pantalla
        self.rect.y = max(0, min(self.rect.y, ALTO - self.rect.height))  # Limitar dentro de la pantalla
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
            self.vel_x = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x =  VELOCIDAD_JUGADOR
            

    def saltar(self):
        # Solo saltar si el jugador está en el suelo.
        if self.en_suelo:
            self.vel_y    = FUERZA_SALTO
            self.en_suelo = False

    def aplicar_gravedad(self):
        # Aplicar gravedad al jugador, limitando la velocidad máxima hacia abajo.
        self.vel_y += GRAVEDAD
        if self.vel_y > 18:
            self.vel_y = 18

    def colision_horizontal(self, plataformas):
        # Detectar colisiones horizontales con plataformas.
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for p in hits:
            if self.vel_x > 0:
                # Ajustar posición si chocamos por la derecha.
                self.rect.right = p.rect.left
            if self.vel_x < 0:
                # Ajustar posición si chocamos por la izquierda.
                self.rect.left  = p.rect.right

    def colision_vertical(self, plataformas):
        # Detectar colisiones verticales y controlar si el jugador está en el suelo.
        self.en_suelo = False
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for p in hits:
            if self.vel_y > 0:
                # Caída sobre la plataforma: posicionar al jugador encima.
                self.rect.bottom = p.rect.top
                self.en_suelo    = True
                self.vel_y       = 0
            if self.vel_y < 0:
                # Rebote de la cabeza contra la parte inferior de una plataforma.
                self.rect.top    = p.rect.bottom
                self.vel_y       = 0
