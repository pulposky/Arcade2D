# Constantes del juego
import pygame

# Dimensiones de la ventana
WIDTH = 1000
HEIGHT = 800
FPS = 60

# Colores (estilo casino clásico)
CASINO_GREEN = (53, 101, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
LIGHT_GREEN = (60, 120, 90)
DARK_GREEN = (40, 80, 60)

# Dimensiones de las cartas
CARD_WIDTH = 70
CARD_HEIGHT = 100
CARD_RADIUS = 8

# Configuración del juego
INITIAL_CHIPS = 1000
MIN_BET = 10
MAX_BET = 500

# Fuentes
pygame.font.init()
TITLE_FONT = pygame.font.Font(None, 48)
LARGE_FONT = pygame.font.Font(None, 36)
MEDIUM_FONT = pygame.font.Font(None, 28)
SMALL_FONT = pygame.font.Font(None, 24)
CARD_FONT = pygame.font.Font(None, 32)