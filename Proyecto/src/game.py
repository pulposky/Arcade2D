import random
import sys
import time

import pygame

from settings import *
from src.enemigo import Enemigo
from src.jugador import Jugador
from src.level_loader import LevelLoader
from src.moneda import Moneda
from src.plataforma import Plataforma
from src.powerup import PowerUp
from src.save_manager import SaveManager


class Game:
    DURACION_POWERUP = 5
    DURACION_INVENCIBLE = 2
    INTERVALO_SPAWN = 3

    def __init__(self, nivel="level_1"):
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 24)
        self.fuente_grande = pygame.font.SysFont("Arial", 48)

        self.save_manager = SaveManager()
        self.level_loader = LevelLoader()
        self.nivel = self.level_loader.cargar(nivel)

        self.todos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self._crear_mundo()
        self._reiniciar_estado()

    def _crear_mundo(self):
        posicion_jugador = self.nivel["jugador"]
        self.jugador = Jugador(posicion_jugador["x"], posicion_jugador["y"])
        self.todos.add(self.jugador)

        for datos in self.nivel["plataformas"]:
            plataforma = Plataforma(
                datos["x"],
                datos["y"],
                datos["ancho"],
                datos["alto"],
            )
            self.todos.add(plataforma)
            self.plataformas.add(plataforma)

        x, y = self._posicion_libre(30, 30)
        self.moneda = Moneda(x, y)
        self.todos.add(self.moneda)

    def _reiniciar_estado(self):
        self.puntaje = 0
        self.vidas = 3
        self.game_over = False
        self.pausado = False
        self.ultimo_spawn = time.time()
        self.record = self.save_manager.cargar_record()
        self.powerup_activo = None
        self.powerup_timer = 0
        self.invencible = False
        self.invencible_timer = 0

    def _posicion_libre(self, ancho=20, alto=20):
        for _ in range(100):
            x = random.randint(50, ANCHO - 50)
            y = random.randint(50, ALTO - 100)
            rect_prueba = pygame.Rect(x, y, ancho, alto)
            if not any(rect_prueba.colliderect(p.rect) for p in self.plataformas):
                return x, y
        return ANCHO // 2, 100

    def reiniciar(self):
        self.enemigos.empty()
        self.powerups.empty()

        for sprite in list(self.todos):
            if isinstance(sprite, (Enemigo, PowerUp)):
                sprite.kill()

        self.jugador.velocidad = VELOCIDAD_JUGADOR
        self.jugador.rect.topleft = (
            self.nivel["jugador"]["x"],
            self.nivel["jugador"]["y"],
        )
        self.jugador.vel_y = 0

        x, y = self._posicion_libre(30, 30)
        self.moneda.rect.center = (x, y)
        self._reiniciar_estado()

    def run(self):
        while True:
            ahora = time.time()
            self._manejar_eventos()

            if not self.game_over and not self.pausado:
                self._actualizar(ahora)

            self._dibujar(ahora)
            pygame.display.flip()
            self.reloj.tick(FPS)

    def _manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado
            elif evento.key == pygame.K_SPACE and not self.game_over and not self.pausado:
                self.jugador.saltar()
            elif evento.key == pygame.K_r and self.game_over:
                self.reiniciar()

    def _actualizar(self, ahora):
        self.jugador.update(self.plataformas)
        self._actualizar_enemigos(ahora)
        self._actualizar_moneda()
        self._actualizar_powerups(ahora)
        self._revisar_colision_enemigos(ahora)

    def _actualizar_enemigos(self, ahora):
        if ahora - self.ultimo_spawn > self.INTERVALO_SPAWN:
            enemigo = Enemigo()
            self.enemigos.add(enemigo)
            self.todos.add(enemigo)
            self.ultimo_spawn = ahora

        for enemigo in self.enemigos:
            enemigo.update(self.jugador)

    def _actualizar_moneda(self):
        if not self.moneda.update(self.jugador):
            return

        self.puntaje += 1

        for enemigo in self.enemigos:
            enemigo.aumentar_velocidad()

        x, y = self._posicion_libre(30, 30)
        self.moneda.rect.center = (x, y)

        if random.random() < 0.5:
            tipo = random.choice(PowerUp.TIPOS)
            px, py = self._posicion_libre()
            powerup = PowerUp(px, py, tipo)
            self.powerups.add(powerup)
            self.todos.add(powerup)

    def _actualizar_powerups(self, ahora):
        recogidos = pygame.sprite.spritecollide(self.jugador, self.powerups, True)
        for powerup in recogidos:
            self.powerup_activo = powerup.tipo
            self.powerup_timer = ahora + self.DURACION_POWERUP
            if powerup.tipo == PowerUp.VELOCIDAD:
                self.jugador.velocidad = VELOCIDAD_JUGADOR * 2

        if self.powerup_activo and ahora > self.powerup_timer:
            if self.powerup_activo == PowerUp.VELOCIDAD:
                self.jugador.velocidad = VELOCIDAD_JUGADOR
            self.powerup_activo = None

    def _revisar_colision_enemigos(self, ahora):
        if self.invencible or self.powerup_activo == PowerUp.INVENCIBLE:
            return

        if not pygame.sprite.spritecollide(self.jugador, self.enemigos, False):
            return

        self.vidas -= 1
        self.invencible = True
        self.invencible_timer = ahora + self.DURACION_INVENCIBLE

        if self.vidas <= 0:
            self.save_manager.guardar_record(self.puntaje)
            self.record = self.save_manager.cargar_record()
            self.game_over = True

    def _dibujar(self, ahora):
        self.ventana.fill(NEGRO)

        if not self.invencible or int(ahora * 6) % 2 == 0:
            self.todos.draw(self.ventana)
        else:
            for sprite in self.todos:
                if sprite != self.jugador:
                    self.ventana.blit(sprite.image, sprite.rect)

        self._dibujar_hud(ahora)

        if self.pausado:
            self._dibujar_pausa()

        if self.game_over:
            self._dibujar_game_over()

        if self.invencible and ahora > self.invencible_timer:
            self.invencible = False

    def _dibujar_hud(self, ahora):
        txt_puntaje = self.fuente.render(f"Puntaje: {self.puntaje}", True, BLANCO)
        txt_record = self.fuente.render(f"Record: {self.record}", True, AMARILLO)
        self.ventana.blit(txt_puntaje, (20, 20))
        self.ventana.blit(txt_record, (20, 50))

        for i in range(self.vidas):
            txt_vida = self.fuente.render("♥", True, ROJO)
            self.ventana.blit(txt_vida, (ANCHO - 40 - i * 30, 20))

        if not self.powerup_activo:
            return

        segundos = max(0, int(self.powerup_timer - ahora))
        color = AMARILLO if self.powerup_activo == PowerUp.VELOCIDAD else CELESTE
        nombre = "Velocidad" if self.powerup_activo == PowerUp.VELOCIDAD else "Invencible"
        txt_powerup = self.fuente.render(f"{nombre} {segundos}s", True, color)
        self.ventana.blit(txt_powerup, (ANCHO // 2 - txt_powerup.get_width() // 2, 20))

    def _dibujar_pausa(self):
        txt_pausa = self.fuente_grande.render("PAUSA", True, BLANCO)
        self.ventana.blit(
            txt_pausa,
            (ANCHO // 2 - txt_pausa.get_width() // 2, ALTO // 2),
        )

    def _dibujar_game_over(self):
        txt_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
        txt_record = self.fuente.render(f"Record: {self.record}", True, AMARILLO)
        txt_reiniciar = self.fuente.render("Presiona R para reiniciar", True, BLANCO)

        self.ventana.blit(
            txt_game_over,
            (ANCHO // 2 - txt_game_over.get_width() // 2, ALTO // 2 - 60),
        )
        self.ventana.blit(
            txt_record,
            (ANCHO // 2 - txt_record.get_width() // 2, ALTO // 2),
        )
        self.ventana.blit(
            txt_reiniciar,
            (ANCHO // 2 - txt_reiniciar.get_width() // 2, ALTO // 2 + 40),
        )
