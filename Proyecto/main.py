# main.py
# Archivo principal del juego de plataformas.
# Inicializa Pygame, crea la ventana, gestiona los sprites y ejecuta el bucle principal.

import pygame
import sys
import random
from settings import *
from src.jugador import Jugador
from src.moneda import Moneda

# Inicialización de Pygame y configuración de la ventana de juego.
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
reloj   = pygame.time.Clock()
fuente  = pygame.font.SysFont('Arial', 24)

# Clase que define una plataforma estática en el mundo de juego.
# Hereda de pygame.sprite.Sprite para poder usar colisiones y dibujo automático.
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(VERDE)
        self.rect  = self.image.get_rect(topleft=(x, y))

# Grupos de sprites para manejo y dibujo colectivo.
todos    = pygame.sprite.Group()
plataformas = pygame.sprite.Group()

# Crear el jugador y añadirlo al grupo principal de sprites.
moneda = Moneda(
    random.randint(50, ANCHO - 50),
    random.randint(50, ALTO - 50)
)
todos.add(moneda)
jugador = Jugador(100, 400)
todos.add(jugador)

# Definición de plataformas fijas: suelo y plataformas intermedias.
datos_plataformas = [
    (0,   560, 800, 40),   # Suelo del nivel
    (100, 420, 200, 20),   # Plataforma 1
    (380, 320, 160, 20),   # Plataforma 2
    (550, 220, 200, 20),   # Plataforma 3
    (300, 120, 90,  20)    # Plataforma 4
]
for datos in datos_plataformas:
    p = Plataforma(*datos)
    todos.add(p)
    plataformas.add(p)

# Variable de ejemplo para mostrar puntaje en pantalla.
puntaje = 0

# Bucle principal del juego: procesa eventos, actualiza lógica y dibuja la escena.
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # Cierre limpio de Pygame y salida del programa.
            pygame.quit(); sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Saltar cuando se pulsa la tecla espacio.
                jugador.saltar()

    # Actualizar el jugador con información de las plataformas para detectar colisiones.
    jugador.update(plataformas)
    puntaje += moneda.update(jugador)

    # Dibujar el fondo, los sprites y la interfaz de puntaje.
    ventana.fill(NEGRO)
    todos.draw(ventana)

    txt = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    ventana.blit(txt, (20, 20))

    # Actualizar la pantalla y sincronizar los FPS.
    pygame.display.flip()
    reloj.tick(FPS)
