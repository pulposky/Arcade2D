from src.card import Deck
from src.player import Player, Dealer
from src.constants import *
import time

class BlackjackGame:
    """Lógica principal del juego de Blackjack"""
    
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.game_state = "BETTING"  # Estados: BETTING, PLAYING, DEALER_TURN, GAME_OVER
        self.message = "Coloca tu apuesta"
        self.round_over = False
        self.dealer_action_time = 0
    
    def start_new_round(self):
        """Inicia una nueva ronda"""
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.round_over = False
        self.dealer_action_time = 0
        
        # Repartir cartas iniciales
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        
        # Ocultar la primera carta del dealer
        self.dealer.hide_first_card()
        
        self.game_state = "PLAYING"
        self.message = "¿Pedir o Plantarse?"
        
        # Verificar blackjack natural
        if self.player.calculate_hand() == 21:
            self.player_stand()
    
    def place_bet(self, amount):
        """Realiza una apuesta"""
        if amount < MIN_BET:
            self.message = f"Apuesta mínima: ${MIN_BET}"
            return False
        if amount > MAX_BET:
            self.message = f"Apuesta máxima: ${MAX_BET}"
            return False
        if amount > self.player.chips:
            self.message = "No tienes suficientes fichas"
            return False
        
        if self.player.place_bet(amount):
            self.start_new_round()
            return True
        return False
    
    def player_hit(self):
        """El jugador pide una carta"""
        if self.game_state != "PLAYING" or self.player.is_standing:
            return
        
        self.player.add_card(self.deck.deal())
        player_value = self.player.calculate_hand()
        
        if player_value > 21:
            self.player.is_busted = True
            self.end_round()
        elif player_value == 21:
            self.player_stand()
    
    def player_stand(self):
        """El jugador se planta"""
        if self.game_state != "PLAYING":
            return
        
        self.player.is_standing = True
        self.dealer.reveal_cards()
        self.game_state = "DEALER_TURN"
        self.message = "Turno del dealer"
        self.dealer_action_time = time.time()
    
    def dealer_turn(self, current_time):
        """Turno automático del dealer"""
        if self.game_state != "DEALER_TURN":
            return
        
        # Esperar un momento antes de cada acción del dealer
        if current_time - self.dealer_action_time < 1.0:
            return
        
        if self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
            self.dealer_action_time = current_time
            
            if self.dealer.calculate_hand() > 21:
                self.dealer.is_busted = True
                self.end_round()
        else:
            self.end_round()
    
    def end_round(self):
        """Finaliza la ronda y determina el ganador"""
        self.game_state = "GAME_OVER"
        self.round_over = True
        
        player_value = self.player.calculate_hand()
        dealer_value = self.dealer.calculate_hand()
        
        # Determinar ganador
        if self.player.is_busted:
            self.message = f"¡Te pasaste! Perdiste ${self.player.lose_bet()}"
        elif self.dealer.is_busted:
            winnings = self.player.win_bet()
            self.message = f"¡El dealer se pasó! Ganaste ${winnings}"
        elif player_value > dealer_value:
            # Blackjack natural paga 2.5x
            if player_value == 21 and len(self.player.hand) == 2:
                winnings = self.player.win_bet(2.5)
                self.message = f"¡BLACKJACK! Ganaste ${winnings}"
            else:
                winnings = self.player.win_bet()
                self.message = f"¡Ganaste! +${winnings}"
        elif player_value < dealer_value:
            self.message = f"Perdiste ${self.player.lose_bet()}"
        else:
            self.player.push_bet()
            self.message = "¡Empate! Apuesta devuelta"
        
        # Verificar si el jugador se quedó sin fichas
        if self.player.chips == 0 and self.player.bet == 0:
            self.message += " | GAME OVER - Sin fichas"
    
    def reset_for_new_bet(self):
        """Reinicia para una nueva apuesta"""
        if self.player.chips == 0:
            self.player.chips = INITIAL_CHIPS
            self.message = "Fichas reiniciadas. Coloca tu apuesta"
        else:
            self.message = "Coloca tu apuesta"
        self.game_state = "BETTING"