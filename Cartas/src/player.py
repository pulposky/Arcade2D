from src.constants import *

class Player:
    """Representa al jugador"""
    
    def __init__(self, chips=INITIAL_CHIPS):
        self.hand = []
        self.chips = chips
        self.bet = 0
        self.is_standing = False
        self.is_busted = False
    
    def add_card(self, card):
        """Agrega una carta a la mano"""
        self.hand.append(card)
    
    def calculate_hand(self):
        """Calcula el valor de la mano considerando los ases"""
        value = 0
        aces = 0
        
        for card in self.hand:
            if not card.hidden:
                card_value = card.get_value()
                value += card_value
                if card.rank == 'A':
                    aces += 1
        
        # Ajustar el valor de los ases si es necesario
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def reset_hand(self):
        """Reinicia la mano para una nueva ronda"""
        self.hand = []
        self.is_standing = False
        self.is_busted = False
    
    def place_bet(self, amount):
        """Realiza una apuesta"""
        if amount <= self.chips:
            self.bet = amount
            self.chips -= amount
            return True
        return False
    
    def win_bet(self, multiplier=2):
        """Gana la apuesta"""
        winnings = self.bet * multiplier
        self.chips += winnings
        self.bet = 0
        return winnings
    
    def lose_bet(self):
        """Pierde la apuesta"""
        lost = self.bet
        self.bet = 0
        return lost
    
    def push_bet(self):
        """Empate, devuelve la apuesta"""
        self.chips += self.bet
        self.bet = 0

class Dealer(Player):
    """Representa al dealer (croupier)"""
    
    def __init__(self):
        super().__init__(chips=0)  # El dealer no tiene fichas
    
    def should_hit(self):
        """El dealer debe pedir carta si tiene menos de 17"""
        return self.calculate_hand() < 17
    
    def hide_first_card(self):
        """Oculta la primera carta del dealer"""
        if len(self.hand) > 0:
            self.hand[0].hidden = True
    
    def reveal_cards(self):
        """Revela todas las cartas del dealer"""
        for card in self.hand:
            card.hidden = False