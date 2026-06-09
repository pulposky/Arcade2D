import array
import math

import pygame


class AudioManager:
    SAMPLE_RATE = 44100

    def __init__(self):
        self.canal_musica = pygame.mixer.Channel(0)
        self.musica_normal = self._crear_tema_normal()
        self.musica_boss = self._crear_tema_boss()
        self.tema_actual = None
        self.canal_musica.set_volume(0.24)

    def play_music(self):
        self._play(self.musica_normal, "normal", 0.24)

    def play_boss_music(self):
        self._play(self.musica_boss, "boss", 0.34)

    def stop_music(self):
        self.canal_musica.stop()
        self.tema_actual = None

    def _play(self, musica, nombre, volumen):
        if self.tema_actual == nombre and self.canal_musica.get_busy():
            return

        self.tema_actual = nombre
        self.canal_musica.set_volume(volumen)
        self.canal_musica.play(musica, loops=-1)

    def _crear_tema_normal(self):
        bpm = 104
        beat = 60 / bpm
        progresion = [
            (196.00, 246.94, 293.66),
            (174.61, 220.00, 261.63),
            (164.81, 196.00, 246.94),
            (146.83, 185.00, 220.00),
        ]
        melodia = [392.00, 329.63, 293.66, 329.63, 392.00, 440.00, 392.00, 293.66]
        return self._crear_loop(bpm, beat * 32, progresion, melodia, modo="normal")

    def _crear_tema_boss(self):
        bpm = 152
        beat = 60 / bpm
        progresion = [
            (110.00, 146.83, 220.00),
            (123.47, 164.81, 246.94),
            (130.81, 174.61, 261.63),
            (98.00, 130.81, 196.00),
        ]
        melodia = [440.00, 415.30, 392.00, 349.23, 329.63, 293.66, 261.63, 220.00]
        return self._crear_loop(bpm, beat * 32, progresion, melodia, modo="boss")

    def _crear_loop(self, bpm, duracion, progresion, melodia, modo):
        beat = 60 / bpm
        total = int(self.SAMPLE_RATE * duracion)
        samples = array.array("h")

        for i in range(total):
            t = i / self.SAMPLE_RATE
            beat_actual = int(t / beat)
            paso = int(t / (beat / 2))
            acorde = progresion[(beat_actual // 4) % len(progresion)]

            if modo == "boss":
                valor = self._sample_boss(t, beat, paso, beat_actual, acorde, melodia)
            else:
                valor = self._sample_normal(t, beat, paso, beat_actual, acorde, melodia)

            samples.append(int(max(-1, min(1, valor)) * 32767))

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _sample_normal(self, t, beat, paso, beat_actual, acorde, melodia):
        nota = melodia[paso % len(melodia)]
        bajo = acorde[0] / 2
        pulso = self._envolvente(t % (beat / 2), beat / 2)

        lead = math.sin(2 * math.pi * nota * t) * 0.20 * pulso
        arpegio = self._triangular(t, acorde[paso % len(acorde)] * 2) * 0.16
        bass = math.sin(2 * math.pi * bajo * t) * 0.26
        clap = 0.18 * self._ruido_perc(t, beat, offset=beat / 2) if beat_actual % 2 else 0

        return lead + arpegio + bass + clap

    def _sample_boss(self, t, beat, paso, beat_actual, acorde, melodia):
        nota = melodia[paso % len(melodia)]
        bajo = acorde[0]
        pulso = self._envolvente(t % (beat / 4), beat / 4)

        lead = self._onda_cuadrada(t, nota) * 0.22 * pulso
        bass = self._onda_cuadrada(t, bajo) * 0.30
        tension = math.sin(2 * math.pi * (nota * 1.5) * t) * 0.10
        kick = 0.48 * self._golpe(t % beat, 0.09, 62)
        snare = 0.22 * self._ruido_perc(t, beat, offset=beat / 2)

        return lead + bass + tension + kick + snare

    def _onda_cuadrada(self, t, frecuencia):
        return 1 if math.sin(2 * math.pi * frecuencia * t) >= 0 else -1

    def _triangular(self, t, frecuencia):
        fase = (t * frecuencia) % 1
        return 4 * abs(fase - 0.5) - 1

    def _envolvente(self, tiempo, duracion):
        return max(0, 1 - tiempo / duracion)

    def _golpe(self, tiempo, duracion, frecuencia):
        if tiempo > duracion:
            return 0
        return math.sin(2 * math.pi * frecuencia * tiempo) * (1 - tiempo / duracion)

    def _ruido_perc(self, t, beat, offset=0):
        tiempo = (t - offset) % beat
        if tiempo > 0.035:
            return 0
        semilla = int(t * self.SAMPLE_RATE)
        ruido = ((semilla * 1103515245 + 12345) % 65536) / 32768 - 1
        return ruido * (1 - tiempo / 0.035)
