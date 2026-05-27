# main.py
import pygame
import sys
import time
import random
import json
import os
from settings import *
from src.jugador import Jugador
from src.moneda import Moneda
from src.enemigo import Enemigo

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
reloj         = pygame.time.Clock()
fuente        = pygame.font.SysFont('Arial', 24)
fuente_grande = pygame.font.SysFont('Arial', 48)

# ─── Clases ───────────────────────────────────────────────────────
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect(topleft=(x, y))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo  = tipo
        self.image = pygame.Surface((20, 20))
        self.image.fill(AMARILLO if tipo == "velocidad" else CELESTE)
        self.rect  = self.image.get_rect(center=(x, y))

# ─── Récord ───────────────────────────────────────────────────────
ARCHIVO_RECORD = "record.json"

def cargar_record():
    if os.path.exists(ARCHIVO_RECORD):
        with open(ARCHIVO_RECORD, "r") as f:
            return json.load(f).get("record", 0)
    return 0

def guardar_record(puntaje):
    record = cargar_record()
    if puntaje > record:
        with open(ARCHIVO_RECORD, "w") as f:
            json.dump({"record": puntaje}, f)

# ─── Posición libre (no dentro de plataformas) ────────────────────
def posicion_libre(plataformas, ancho=20, alto=20):
    for _ in range(100):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(50, ALTO - 100)
        rect_prueba = pygame.Rect(x, y, ancho, alto)
        if not any(rect_prueba.colliderect(p.rect) for p in plataformas):
            return x, y
    return ANCHO // 2, 100

# ─── Datos de plataformas iniciales ───────────────────────────────
datos_plataformas = [
    (0,   560, 800, 40),   # Suelo
    (100, 420, 200, 20),   # Plataforma 1 
    (200, 210, 160, 20),   # Plataforma 2 
    (380, 320, 160, 20),   # Plataforma 3 
    (580, 260, 160, 20),   # Plataforma 4 
    (400, 140, 140, 20),   # Plataforma 5 
    (615,  70, 160, 20),   # Plataforma 6 
]

# ─── Grupos ───────────────────────────────────────────────────────
todos       = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
enemigos    = pygame.sprite.Group()
powerups    = pygame.sprite.Group()

# ─── Sprites iniciales ────────────────────────────────────────────
jugador = Jugador(100, 400)
todos.add(jugador)

for datos in datos_plataformas:
    p = Plataforma(*datos)
    todos.add(p)
    plataformas.add(p)

x, y = posicion_libre(plataformas, 30, 30)
moneda = Moneda(x, y)
todos.add(moneda)

# ─── Variables de estado ──────────────────────────────────────────
puntaje          = 0
vidas            = 3
game_over        = False
pausado          = False
ultimo_spawn     = time.time()
intervalo_spawn  = 3
record           = cargar_record()
powerup_activo   = None
powerup_timer    = 0
DURACION_POWERUP = 5
invencible       = False
invencible_timer = 0
DURACION_INV     = 2

# ─── Reinicio ─────────────────────────────────────────────────────
def reiniciar():
    global puntaje, vidas, game_over, ultimo_spawn
    global powerup_activo, powerup_timer, invencible, invencible_timer, record

    for e in list(enemigos):
        todos.remove(e)
    enemigos.empty()

    for pw in list(powerups):
        todos.remove(pw)
    powerups.empty()

    if powerup_activo == "velocidad":
        jugador.vel_x = 0

    x, y = posicion_libre(plataformas, 30, 30)
    moneda.rect.center = (x, y)

    jugador.rect.topleft = (100, 400)
    jugador.vel_y        = 0

    puntaje          = 0
    vidas            = 3
    game_over        = False
    ultimo_spawn     = time.time()
    powerup_activo   = None
    powerup_timer    = 0
    invencible       = False
    invencible_timer = 0
    record           = cargar_record()

# ─── Bucle principal ──────────────────────────────────────────────
while True:
    ahora = time.time()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pausado = not pausado
            if evento.key == pygame.K_SPACE and not game_over and not pausado:
                jugador.saltar()
            if evento.key == pygame.K_r and game_over:
                reiniciar()

    if not game_over and not pausado:
        jugador.update(plataformas)

        # ── Spawn enemigos ────────────────────────────────────────
        if ahora - ultimo_spawn > intervalo_spawn:
            nuevo = Enemigo()
            enemigos.add(nuevo)
            todos.add(nuevo)
            ultimo_spawn = ahora

        for enemigo in enemigos:
            enemigo.update(jugador)

        # ── Moneda ────────────────────────────────────────────────
        moneda_recogida = moneda.update(jugador)
        if moneda_recogida:
            puntaje += 1
            for e in enemigos:
                e.aumentar_velocidad()

            # Reubicar moneda en posición libre
            x, y = posicion_libre(plataformas, 30, 30)
            moneda.rect.center = (x, y)

            # 30% de probabilidad de spawnear power-up
            if random.random() < 0.3:
                tipo  = random.choice(["velocidad", "invencible"])
                px, py = posicion_libre(plataformas)
                pw    = PowerUp(px, py, tipo)
                powerups.add(pw)
                todos.add(pw)

        # ── Power-ups ─────────────────────────────────────────────
        recogidos = pygame.sprite.spritecollide(jugador, powerups, True)
        for pw in recogidos:
            todos.remove(pw)
            powerup_activo = pw.tipo
            powerup_timer  = ahora + DURACION_POWERUP
            if pw.tipo == "velocidad":
                jugador.vel_x = 0  # resetear para que tome efecto limpio

        if powerup_activo and ahora > powerup_timer:
            powerup_activo = None

        # ── Colisión con enemigos ─────────────────────────────────
        if not invencible and powerup_activo != "invencible":
            if pygame.sprite.spritecollide(jugador, enemigos, False):
                vidas -= 1
                invencible       = True
                invencible_timer = ahora + DURACION_INV
                if vidas <= 0:
                    guardar_record(puntaje)
                    record    = cargar_record()
                    game_over = True

        if invencible and ahora > invencible_timer:
            invencible = False

    # ── Dibujar ───────────────────────────────────────────────────
    ventana.fill(NEGRO)

    if not invencible or int(ahora * 6) % 2 == 0:
        todos.draw(ventana)
    else:
        for sprite in todos:
            if sprite != jugador:
                ventana.blit(sprite.image, sprite.rect)

    enemigos.draw(ventana)
    powerups.draw(ventana)

    # HUD
    txt_puntaje = fuente.render(f'Puntaje: {puntaje}', True, BLANCO)
    txt_record  = fuente.render(f'Récord: {record}',   True, AMARILLO)
    ventana.blit(txt_puntaje, (20, 20))
    ventana.blit(txt_record,  (20, 50))

    for i in range(vidas):
        txt_vida = fuente.render('♥', True, ROJO)
        ventana.blit(txt_vida, (ANCHO - 40 - i * 30, 20))

    if powerup_activo:
        segundos = max(0, int(powerup_timer - ahora))
        color    = AMARILLO if powerup_activo == "velocidad" else CELESTE
        nombre   = "⚡ Velocidad" if powerup_activo == "velocidad" else "🛡 Invencible"
        txt_pw   = fuente.render(f'{nombre} {segundos}s', True, color)
        ventana.blit(txt_pw, (ANCHO//2 - txt_pw.get_width()//2, 20))

    if pausado:
        txt_pausa = fuente_grande.render('PAUSA', True, BLANCO)
        ventana.blit(txt_pausa, (ANCHO//2 - txt_pausa.get_width()//2, ALTO//2))

    if game_over:
        go      = fuente_grande.render('GAME OVER', True, ROJO)
        rec_txt = fuente.render(f'Récord: {record}', True, AMARILLO)
        rst     = fuente.render('Presiona R para reiniciar', True, BLANCO)
        ventana.blit(go,      (ANCHO//2 - go.get_width()//2,      ALTO//2 - 60))
        ventana.blit(rec_txt, (ANCHO//2 - rec_txt.get_width()//2, ALTO//2))
        ventana.blit(rst,     (ANCHO//2 - rst.get_width()//2,     ALTO//2 + 40))

    pygame.display.flip()
    reloj.tick(FPS)