import pygame
import sys
from settings import *
from src.jugador import Jugador

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
reloj   = pygame.time.Clock()
fuente  = pygame.font.SysFont('Arial', 24)

# Clase plataforma simple
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(VERDE)
        self.rect  = self.image.get_rect(topleft=(x, y))

# Crear sprites
todos    = pygame.sprite.Group()
plataformas = pygame.sprite.Group()

jugador = Jugador(100, 400)
todos.add(jugador)

datos_plataformas = [
    (0,   560, 800, 40),   # Suelo
    (100, 420, 200, 20),   # Plataforma 1
    (380, 320, 160, 20),   # Plataforma 2
    (550, 220, 200, 20),   # Plataforma 3
]
for datos in datos_plataformas:
    p = Plataforma(*datos)
    todos.add(p)
    plataformas.add(p)

puntaje = 0

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.saltar()

    jugador.update(plataformas)

    ventana.fill(NEGRO)
    todos.draw(ventana)

    txt = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    ventana.blit(txt, (20, 20))

    pygame.display.flip()
    reloj.tick(FPS)
