import pygame

from settings import ROJO


class Corazon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ROJO, (8, 9), 7)
        pygame.draw.circle(self.image, ROJO, (16, 9), 7)
        pygame.draw.polygon(self.image, ROJO, [(2, 12), (22, 12), (12, 24)])
        self.rect = self.image.get_rect(center=(x, y))
