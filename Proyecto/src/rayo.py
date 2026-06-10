import pygame

from settings import CELESTE


class Rayo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = pygame.Surface((12, 36))
        self.image.fill(CELESTE)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 7
        self.direccion = direccion

    def update(self):
        dx, dy = self.direccion
        self.rect.x += int(dx * self.velocidad)
        self.rect.y += int(dy * self.velocidad)
