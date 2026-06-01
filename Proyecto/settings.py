# settings.py
# Configuración global del juego que define tamaños, colores y físicas básicas.

# Tamaño de la ventana del juego en píxeles.
ANCHO  = 800
ALTO   = 600
# Velocidad de fotogramas objetivo para sincronizar el juego.
FPS    = 60
# Título mostrado en la ventana del juego.
TITULO = 'Plataformas'

# Colores principales usados en el juego en formato RGB.
NEGRO  = (0,   0,   0)
BLANCO = (255, 255, 255)
AZUL   = (0,   120, 255)
VERDE  = (50,  200, 50)
ROJO   = (220, 50,  50)
GRIS   = (80,  80,  80)
AMARILLO = (255, 215, 0)
CELESTE  = (0, 200, 255)

# Constantes de movimiento del jugador.
# VELOCIDAD_JUGADOR controla la velocidad horizontal.
# FUERZA_SALTO define el impulso inicial hacia arriba al saltar.
# GRAVEDAD aplica aceleración constante hacia abajo.
VELOCIDAD_JUGADOR = 5
FUERZA_SALTO      = -16
GRAVEDAD          = 0.6