"""
Juego de Blackjack (21) usando Pygame
Estilo Casino Clásico

Controles:
    - H o SPACE: Pedir carta
    - S o ENTER: Plantarse
    - O usa los botones en pantalla
"""

from src.ui import BlackjackUI

def main():
    game = BlackjackUI()
    game.run()

if __name__ == "__main__":
    main()