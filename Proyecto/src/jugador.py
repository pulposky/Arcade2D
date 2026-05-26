import pygame
from settings import *

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(AZUL)
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = False

    def update(self, plataformas):
        self.mover()
        self.aplicar_gravedad()
        self.rect.x += self.vel_x
        self.colision_horizontal(plataformas)
        self.rect.y += self.vel_y
        self.colision_vertical(plataformas)

    def mover(self):
        teclas = pygame.key.get_pressed()
        self.vel_x = 0
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
            self.vel_x = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x =  VELOCIDAD_JUGADOR

    def saltar(self):
        if self.en_suelo:
            self.vel_y    = FUERZA_SALTO
            self.en_suelo = False

    def aplicar_gravedad(self):
        self.vel_y += GRAVEDAD
        if self.vel_y > 18: self.vel_y = 18

    def colision_horizontal(self, plataformas):
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for p in hits:
            if self.vel_x > 0: self.rect.right = p.rect.left
            if self.vel_x < 0: self.rect.left  = p.rect.right

    def colision_vertical(self, plataformas):
        self.en_suelo = False
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for p in hits:
            if self.vel_y > 0:
                self.rect.bottom = p.rect.top
                self.en_suelo    = True
                self.vel_y       = 0
            if self.vel_y < 0:
                self.rect.top    = p.rect.bottom
                self.vel_y       = 0

