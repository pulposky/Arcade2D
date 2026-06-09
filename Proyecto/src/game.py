import random
import sys
import time

import pygame

from settings import *
from src.audio_manager import AudioManager
from src.boss import Boss
from src.corazon import Corazon
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
    MAX_VIDAS = 5
    DANO_POWERUP_BOSS = 3

    def __init__(self, nivel="level_1"):
        pygame.mixer.pre_init(AudioManager.SAMPLE_RATE, -16, 1, 512)
        pygame.init()
        self.ancho_ventana = ANCHO
        self.ventana = self._crear_ventana()
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Arial", 24)
        self.fuente_grande = pygame.font.SysFont("Arial", 48)
        self.audio = AudioManager()
        self.audio.play_music()

        self.save_manager = SaveManager()
        self.level_loader = LevelLoader()
        self.nivel = self.level_loader.cargar(nivel)

        self.todos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.corazones = pygame.sprite.Group()
        self.rayos = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()

        self._reiniciar_estado()
        self._crear_mundo()
        self.audio.play_music()

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
        self.ancho_mundo = ANCHO_MUNDO_INICIAL
        self.camara_x = 0
        self.siguiente_expansion = 10
        self.siguiente_corazon = 5
        self.siguiente_boss = 20
        self.dificultad_boss = 1
        self.boss = None
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
            x = random.randint(50, self.ancho_mundo - 50)
            y = random.randint(50, ALTO - 100)
            rect_prueba = pygame.Rect(x, y, ancho, alto)
            if self._rect_libre(rect_prueba):
                return x, y
        return ANCHO // 2, 100

    def _rect_libre(self, rect, margen=12):
        rect_con_margen = rect.inflate(margen * 2, margen * 2)
        return not any(rect_con_margen.colliderect(p.rect) for p in self.plataformas)

    def reiniciar(self):
        self.ancho_ventana = ANCHO
        self.ventana = self._crear_ventana()
        self.todos.empty()
        self.plataformas.empty()
        self.enemigos.empty()
        self.powerups.empty()
        self.corazones.empty()
        self.rayos.empty()
        self.bosses.empty()

        self._reiniciar_estado()
        self._crear_mundo()

    def run(self):
        while True:
            ahora = time.time()
            self._manejar_eventos()

            if not self.game_over and not self.pausado:
                self._actualizar(ahora)

            self._dibujar(ahora)
            pygame.display.flip()
            self.reloj.tick(FPS)

    def _crear_ventana(self):
        return pygame.display.set_mode(
            (self.ancho_ventana, ALTO),
            pygame.FULLSCREEN | pygame.SCALED,
        )

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
        self.jugador.update(self.plataformas, self.ancho_mundo)
        self._actualizar_camara()
        self._actualizar_boss()
        if not self.boss:
            self._actualizar_enemigos(ahora)
        self._actualizar_moneda()
        self._actualizar_corazones()
        self._actualizar_powerups(ahora)
        self._revisar_colision_enemigos(ahora)
        self._revisar_colision_rayos(ahora)

    def _actualizar_camara(self):
        objetivo = self.jugador.rect.centerx - self.ancho_ventana // 2
        self.camara_x = max(0, min(objetivo, self.ancho_mundo - self.ancho_ventana))

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
        self._revisar_progresion()

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

    def _revisar_progresion(self):
        if self.puntaje >= self.siguiente_expansion and self.puntaje <= 50:
            self._expandir_mundo()
            self.siguiente_expansion += 10

        if not self.boss and self.puntaje >= self.siguiente_corazon:
            self._crear_corazon()
            self.siguiente_corazon += 5

        if not self.boss and self.puntaje >= self.siguiente_boss:
            self._iniciar_boss()

    def _expandir_mundo(self):
        ancho_anterior = self.ancho_mundo
        self.ancho_mundo = min(
            ANCHO_MUNDO_MAXIMO,
            self.ancho_mundo + EXPANSION_MUNDO,
        )
        if self.ancho_mundo == ancho_anterior:
            return

        self._ampliar_ventana()

        suelo = Plataforma(ancho_anterior, ALTO - 40, self.ancho_mundo - ancho_anterior, 40)
        self.todos.add(suelo)
        self.plataformas.add(suelo)

        self._crear_plataformas_expansion(ancho_anterior)

    def _crear_plataformas_expansion(self, x_inicio):
        cantidad = random.randint(2, 4)
        creadas = 0
        intentos = 0

        while creadas < cantidad and intentos < 80:
            intentos += 1
            ancho = random.randint(110, 190)
            alto = 20
            x = random.randint(x_inicio + 35, self.ancho_mundo - ancho - 35)
            y = random.choice([110, 170, 230, 290, 350, 410])
            rect = pygame.Rect(x, y, ancho, alto)

            if not self._plataforma_valida(rect):
                continue

            plataforma = Plataforma(x, y, ancho, alto)
            self.todos.add(plataforma)
            self.plataformas.add(plataforma)
            creadas += 1

    def _plataforma_valida(self, rect):
        if rect.bottom >= ALTO - 70:
            return False

        if not self._rect_libre(rect, margen=45):
            return False

        plataforma_cercana = False
        zona_apoyo = pygame.Rect(rect.x - 90, rect.y + 45, rect.width + 180, 120)
        for plataforma in self.plataformas:
            if zona_apoyo.colliderect(plataforma.rect):
                plataforma_cercana = True
                break

        return plataforma_cercana

    def _ampliar_ventana(self):
        nuevo_ancho = min(
            ANCHO_VENTANA_MAXIMO,
            self.ancho_ventana + EXPANSION_MUNDO // 2,
            self.ancho_mundo,
        )
        if nuevo_ancho == self.ancho_ventana:
            return

        self.ancho_ventana = nuevo_ancho
        self.ventana = self._crear_ventana()

    def _crear_corazon(self):
        if self.vidas >= self.MAX_VIDAS:
            return

        x, y = self._posicion_libre(24, 24)
        corazon = Corazon(x, y)
        self.corazones.add(corazon)
        self.todos.add(corazon)

    def _actualizar_corazones(self):
        recogidos = pygame.sprite.spritecollide(self.jugador, self.corazones, True)
        if recogidos:
            self.vidas = min(self.MAX_VIDAS, self.vidas + len(recogidos))

    def _iniciar_boss(self):
        self._limpiar_grupo(self.enemigos)
        self._limpiar_grupo(self.corazones)
        self._limpiar_grupo(self.rayos)
        self.boss = Boss(self.ancho_mundo, self.dificultad_boss)
        self.bosses.add(self.boss)
        self.todos.add(self.boss)
        self.audio.play_boss_music()

    def _actualizar_boss(self):
        if not self.boss:
            return

        self.boss.update(self.ancho_mundo, self.jugador, self.rayos)
        for rayo in self.rayos:
            rayo.update()
            if (
                rayo.rect.right < 0
                or rayo.rect.left > self.ancho_mundo
                or rayo.rect.bottom < 0
                or rayo.rect.top > ALTO
            ):
                rayo.kill()

    def _derrotar_boss(self):
        self.boss.kill()
        self.boss = None
        self._limpiar_grupo(self.rayos)
        self.dificultad_boss += 1
        self.siguiente_boss += 100
        self.siguiente_corazon = ((self.puntaje // 5) + 1) * 5
        self.ultimo_spawn = time.time()
        self.audio.play_music()

    def _limpiar_grupo(self, grupo):
        for sprite in list(grupo):
            sprite.kill()

    def _actualizar_powerups(self, ahora):
        recogidos = pygame.sprite.spritecollide(self.jugador, self.powerups, True)
        for powerup in recogidos:
            if self.boss:
                if self.boss.recibir_dano(self.DANO_POWERUP_BOSS):
                    self._derrotar_boss()
                continue

            self.powerup_activo = powerup.tipo
            self.powerup_timer = ahora + self.DURACION_POWERUP
            if powerup.tipo == PowerUp.VELOCIDAD:
                self.jugador.velocidad = VELOCIDAD_JUGADOR * 2

        if self.powerup_activo and ahora > self.powerup_timer:
            if self.powerup_activo == PowerUp.VELOCIDAD:
                self.jugador.velocidad = VELOCIDAD_JUGADOR
            self.powerup_activo = None

    def _revisar_colision_enemigos(self, ahora):
        if self.boss:
            return

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

    def _revisar_colision_rayos(self, ahora):
        if not self.boss:
            return

        if self.invencible or self.powerup_activo == PowerUp.INVENCIBLE:
            return

        if not pygame.sprite.spritecollide(self.jugador, self.rayos, True):
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
            self._dibujar_sprites(self.todos)
        else:
            for sprite in self.todos:
                if sprite != self.jugador:
                    self._dibujar_sprite(sprite)

        self._dibujar_sprites(self.rayos)
        if self.boss:
            self.boss.dibujar_barra_vida(self.ventana, self.camara_x)

        self._dibujar_hud(ahora)

        if self.pausado:
            self._dibujar_pausa()

        if self.game_over:
            self._dibujar_game_over()

        if self.invencible and ahora > self.invencible_timer:
            self.invencible = False

    def _dibujar_sprites(self, grupo):
        for sprite in grupo:
            self._dibujar_sprite(sprite)

    def _dibujar_sprite(self, sprite):
        self.ventana.blit(sprite.image, sprite.rect.move(-self.camara_x, 0))

    def _dibujar_hud(self, ahora):
        txt_puntaje = self.fuente.render(f"Puntaje: {self.puntaje}", True, BLANCO)
        txt_record = self.fuente.render(f"Record: {self.record}", True, AMARILLO)
        txt_mundo = self.fuente.render(f"Mapa: {self.ancho_mundo}px", True, GRIS)
        self.ventana.blit(txt_puntaje, (20, 20))
        self.ventana.blit(txt_record, (20, 50))
        self.ventana.blit(txt_mundo, (20, 80))

        for i in range(self.vidas):
            txt_vida = self.fuente.render("♥", True, ROJO)
            self.ventana.blit(txt_vida, (self.ancho_ventana - 40 - i * 30, 20))

        if not self.powerup_activo:
            return

        segundos = max(0, int(self.powerup_timer - ahora))
        color = AMARILLO if self.powerup_activo == PowerUp.VELOCIDAD else CELESTE
        nombre = "Velocidad" if self.powerup_activo == PowerUp.VELOCIDAD else "Invencible"
        txt_powerup = self.fuente.render(f"{nombre} {segundos}s", True, color)
        self.ventana.blit(
            txt_powerup,
            (self.ancho_ventana // 2 - txt_powerup.get_width() // 2, 20),
        )

    def _dibujar_pausa(self):
        txt_pausa = self.fuente_grande.render("PAUSA", True, BLANCO)
        self.ventana.blit(
            txt_pausa,
            (self.ancho_ventana // 2 - txt_pausa.get_width() // 2, ALTO // 2),
        )

    def _dibujar_game_over(self):
        txt_game_over = self.fuente_grande.render("GAME OVER", True, ROJO)
        txt_record = self.fuente.render(f"Record: {self.record}", True, AMARILLO)
        txt_reiniciar = self.fuente.render("Presiona R para reiniciar", True, BLANCO)

        self.ventana.blit(
            txt_game_over,
            (self.ancho_ventana // 2 - txt_game_over.get_width() // 2, ALTO // 2 - 60),
        )
        self.ventana.blit(
            txt_record,
            (self.ancho_ventana // 2 - txt_record.get_width() // 2, ALTO // 2),
        )
        self.ventana.blit(
            txt_reiniciar,
            (self.ancho_ventana // 2 - txt_reiniciar.get_width() // 2, ALTO // 2 + 40),
        )
