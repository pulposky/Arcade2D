import pygame

from settings import AMARILLO, CELESTE


class PowerUp(pygame.sprite.Sprite):
    VELOCIDAD = "velocidad"
    INVENCIBLE = "invencible"
    TIPOS = (VELOCIDAD, INVENCIBLE)

    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((20, 20))
        self.image.fill(AMARILLO if tipo == self.VELOCIDAD else CELESTE)
        self.rect = self.image.get_rect(center=(x, y))
