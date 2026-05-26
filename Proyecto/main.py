# main.py
# Archivo principal del juego de plataformas.
# Inicializa Pygame, crea la ventana, gestiona los sprites y ejecuta el bucle principal.

import pygame
import sys
import time
import random
from settings import *
from src.jugador import Jugador
from src.moneda import Moneda
from src.enemigo import Enemigo

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

enemigos       = pygame.sprite.Group()
ultimo_spawn   = time.time()
intervalo_spawn = 3  # segundos entre cada enemigo
game_over      = False
pausado = False

# Definición de plataformas fijas: suelo y plataformas intermedias.
datos_plataformas = [
    (0,   560, 800, 40),   # Suelo del nivel
    (100, 420, 200, 20),   # Plataforma 1
    (380, 320, 160, 20),   # Plataforma 2
    (550, 220, 200, 20),   # Plataforma 3
    (300, 120, 90,  20),    # Plataforma 4
    (580, 420, 90,  20)    # Plataforma 5
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
            pygame.quit(); sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pausado = not pausado
            if evento.key == pygame.K_SPACE and not game_over:
                jugador.saltar()
            if evento.key == pygame.K_r and game_over:
                # Eliminar enemigos de AMBOS grupos
                for e in enemigos:
                    todos.remove(e)
                enemigos.empty()
                
                jugador.rect.topleft = (100, 400)
                puntaje = 0
                game_over = False

    if not game_over and not pausado:
        jugador.update(plataformas)

        # Spawn de enemigos cada X segundos
        if time.time() - ultimo_spawn > intervalo_spawn:
            nuevo = Enemigo()
            enemigos.add(nuevo)
            todos.add(nuevo)
            ultimo_spawn = time.time()

        for enemigo in enemigos:
            enemigo.update(jugador)

        moneda_recogida = moneda.update(jugador)
        puntaje += moneda_recogida
        if moneda_recogida:
            for e in enemigos:
                e.aumentar_velocidad()

        # Comprobar colisión con cualquier enemigo
        if pygame.sprite.spritecollide(jugador, enemigos, False):
            game_over = True

    # Dibujar
    ventana.fill(NEGRO)
    todos.draw(ventana)
    enemigos.draw(ventana)

    txt = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    ventana.blit(txt, (20, 20))
    
    if pausado:
        txt_pausa = fuente.render('PAUSA', True, BLANCO)
        ventana.blit(txt_pausa, (ANCHO//2 - txt_pausa.get_width()//2, ALTO//2))
    
    if game_over:
        go  = fuente.render('GAME OVER', True, ROJO)
        rst = fuente.render('Presiona R para reiniciar', True, BLANCO)
        ventana.blit(go,  (ANCHO//2 - go.get_width()//2,  ALTO//2 - 30))
        ventana.blit(rst, (ANCHO//2 - rst.get_width()//2, ALTO//2 + 10))

    pygame.display.flip()
    reloj.tick(FPS)