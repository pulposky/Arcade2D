import random
import pygame
from src.constants import *

class Card:
    """Representa una carta de la baraja"""
    
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.hidden = False
        
    def get_value(self):
        """Obtiene el valor numérico de la carta"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # El As puede valer 1 u 11, se ajusta en calculate_hand
        else:
            return int(self.rank)
    
    def is_red(self):
        """Verifica si la carta es roja"""
        return self.suit in ['♥', '♦']
    
    def draw(self, surface, x, y):
        """Dibuja la carta en la superficie"""
        if self.hidden:
            # Carta boca abajo (reverso)
            pygame.draw.rect(surface, DARK_GREEN, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=CARD_RADIUS)
            pygame.draw.rect(surface, GOLD, (x, y, CARD_WIDTH, CARD_HEIGHT), 3, border_radius=CARD_RADIUS)
            # Patrón en el reverso
            for i in range(3):
                for j in range(4):
                    pygame.draw.circle(surface, GOLD, (x + 20 + i * 15, y + 20 + j * 20), 3)
        else:
            # Carta boca arriba
            pygame.draw.rect(surface, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=CARD_RADIUS)
            pygame.draw.rect(surface, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=CARD_RADIUS)
            
            # Color del texto según el palo
            color = RED if self.is_red() else BLACK
            
            # Dibujar rank y suit
            rank_text = CARD_FONT.render(self.rank, True, color)
            suit_text = CARD_FONT.render(self.suit, True, color)
            
            # Rank en la esquina superior izquierda
            surface.blit(rank_text, (x + 5, y + 5))
            # Suit en el centro
            suit_rect = suit_text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
            surface.blit(suit_text, suit_rect)
            # Rank en la esquina inferior derecha (invertido)
            rank_text_bottom = pygame.transform.rotate(rank_text, 180)
            surface.blit(rank_text_bottom, (x + CARD_WIDTH - rank_text.get_width() - 5, 
                                        y + CARD_HEIGHT - rank_text.get_height() - 5))

class Deck:
    """Representa una baraja de cartas"""
    
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """Reinicia la baraja con todas las cartas"""
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))
        self.shuffle()
    
    def shuffle(self):
        """Mezcla la baraja"""
        random.shuffle(self.cards)
    
    def deal(self):
        """Reparte una carta"""
        if len(self.cards) < 15:  # Reiniciar si quedan pocas cartas
            self.reset()
        return self.cards.pop()