import pygame
import sys
from src.constants import *
from src.game import BlackjackGame
import time

class BlackjackUI:
    """Interfaz gráfica del juego usando Pygame"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Blackjack - Casino 21")
        self.clock = pygame.time.Clock()
        self.game = BlackjackGame()
        self.bet_input = ""
        self.quick_bet_amounts = [10, 25, 50, 100, 250, 500]
    
    def draw_table(self):
        """Dibuja la mesa de casino"""
        self.screen.fill(CASINO_GREEN)
        
        # Título
        title = TITLE_FONT.render("♠ BLACKJACK ♥", True, GOLD)
        title_rect = title.get_rect(center=(WIDTH // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Línea decorativa
        pygame.draw.rect(self.screen, GOLD, (50, 80, WIDTH - 100, 3))
    
    def draw_cards(self, hand, x, y, label):
        """Dibuja las cartas de una mano"""
        # Etiqueta
        label_text = MEDIUM_FONT.render(label, True, WHITE)
        self.screen.blit(label_text, (x, y - 30))
        
        # Cartas
        for i, card in enumerate(hand):
            card_x = x + i * (CARD_WIDTH + 10)
            card.draw(self.screen, card_x, y)
        
        # Valor de la mano
        if label == "DEALER" and self.game.game_state == "PLAYING":
            # Solo mostrar la carta visible del dealer
            visible_value = 0
            for card in hand:
                if not card.hidden:
                    visible_value = card.get_value()
                    break
            value_text = SMALL_FONT.render(f"Mostrando: {visible_value}", True, WHITE)
        else:
            value = self.game.dealer.calculate_hand() if label == "DEALER" else self.game.player.calculate_hand()
            value_text = SMALL_FONT.render(f"Total: {value}", True, GOLD if value == 21 else WHITE)
        
        self.screen.blit(value_text, (x, y + CARD_HEIGHT + 10))
    
    def draw_button(self, text, x, y, width, height, color, hover_color, action=None):
        """Dibuja un botón interactivo"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        button_rect = pygame.Rect(x, y, width, height)
        
        # Efecto hover
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, hover_color, button_rect, border_radius=8)
            if click[0] == 1 and action:
                pygame.time.wait(100)
                return action()
        else:
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
        
        # Borde
        pygame.draw.rect(self.screen, GOLD, button_rect, 3, border_radius=8)
        
        # Texto
        text_surf = MEDIUM_FONT.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return False
    
    def draw_betting_screen(self):
        """Dibuja la pantalla de apuestas"""
        # Fichas del jugador
        chips_text = LARGE_FONT.render(f"Fichas: ${self.game.player.chips}", True, GOLD)
        self.screen.blit(chips_text, (WIDTH // 2 - chips_text.get_width() // 2, 150))
        
        # Apuestas rápidas
        y_start = 250
        quick_bet_label = MEDIUM_FONT.render("Apuestas Rápidas:", True, WHITE)
        self.screen.blit(quick_bet_label, (WIDTH // 2 - quick_bet_label.get_width() // 2, y_start))
        
        for i, amount in enumerate(self.quick_bet_amounts):
            row = i // 3
            col = i % 3
            x = WIDTH // 2 - 180 + col * 120
            y = y_start + 50 + row * 70
            
            if amount <= self.game.player.chips:
                self.draw_button(f"${amount}", x, y, 100, 50, DARK_GREEN, LIGHT_GREEN, 
                            lambda amt=amount: self.game.place_bet(amt))
            else:
                # Botón deshabilitado
                pygame.draw.rect(self.screen, GRAY, (x, y, 100, 50), border_radius=8)
                text = SMALL_FONT.render(f"${amount}", True, BLACK)
                self.screen.blit(text, (x + 50 - text.get_width() // 2, y + 25 - text.get_height() // 2))
        
        # Apuesta personalizada
        custom_label = MEDIUM_FONT.render("O ingresa un monto:", True, WHITE)
        self.screen.blit(custom_label, (WIDTH // 2 - custom_label.get_width() // 2, 450))
        
        # Input de apuesta
        input_rect = pygame.Rect(WIDTH // 2 - 100, 490, 200, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, GOLD, input_rect, 3, border_radius=5)
        
        bet_text = MEDIUM_FONT.render(f"${self.bet_input}", True, BLACK)
        self.screen.blit(bet_text, (input_rect.x + 10, input_rect.y + 8))
        
        # Botón confirmar
        self.draw_button("APOSTAR", WIDTH // 2 - 75, 550, 150, 50, DARK_GREEN, LIGHT_GREEN,
                        lambda: self.confirm_bet())
    
    def confirm_bet(self):
        """Confirma la apuesta personalizada"""
        try:
            if self.bet_input:
                amount = int(self.bet_input)
                self.game.place_bet(amount)
                self.bet_input = ""
        except ValueError:
            self.game.message = "Ingresa un número válido"
    
    def draw_game_screen(self):
        """Dibuja la pantalla de juego"""
        # Dealer
        self.draw_cards(self.game.dealer.hand, 100, 120, "DEALER")
        
        # Jugador
        self.draw_cards(self.game.player.hand, 100, 400, "JUGADOR")
        
        # Info de apuesta y fichas
        info_x = WIDTH - 280
        info_y = 150
        
        pygame.draw.rect(self.screen, DARK_GREEN, (info_x - 10, info_y - 10, 260, 200), border_radius=10)
        pygame.draw.rect(self.screen, GOLD, (info_x - 10, info_y - 10, 260, 200), 3, border_radius=10)
        
        bet_text = MEDIUM_FONT.render(f"Apuesta: ${self.game.player.bet}", True, WHITE)
        chips_text = MEDIUM_FONT.render(f"Fichas: ${self.game.player.chips}", True, GOLD)
        
        self.screen.blit(bet_text, (info_x, info_y))
        self.screen.blit(chips_text, (info_x, info_y + 40))
        
        # Botones de acción
        if self.game.game_state == "PLAYING" and not self.game.player.is_standing:
            self.draw_button("PEDIR", info_x, info_y + 90, 120, 50, DARK_GREEN, LIGHT_GREEN,
                        lambda: self.game.player_hit())
            self.draw_button("PLANTARSE", info_x, info_y + 150, 120, 50, DARK_GREEN, LIGHT_GREEN,
                        lambda: self.game.player_stand())
        
        # Mensaje de estado
        msg_bg_rect = pygame.Rect(50, HEIGHT - 80, WIDTH - 150, 60)
        pygame.draw.rect(self.screen, DARK_GREEN, msg_bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, msg_bg_rect, 3, border_radius=10)
        
        message = MEDIUM_FONT.render(self.game.message, True, WHITE)
        self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 60))
        
        # Botón de nueva ronda si el juego terminó
        if self.game.game_state == "GAME_OVER":
            self.draw_button("NUEVA RONDA", WIDTH // 2 - 100, HEIGHT - 150, 200, 50, 
                        DARK_GREEN, LIGHT_GREEN, lambda: self.game.reset_for_new_bet())
    
    def handle_events(self):
        """Maneja los eventos de pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game.game_state == "BETTING":
                    if event.key == pygame.K_RETURN:
                        self.confirm_bet()
                    elif event.key == pygame.K_BACKSPACE:
                        self.bet_input = self.bet_input[:-1]
                    elif event.unicode.isdigit() and len(self.bet_input) < 4:
                        self.bet_input += event.unicode
                
                # Atajos de teclado durante el juego
                if self.game.game_state == "PLAYING":
                    if event.key == pygame.K_h or event.key == pygame.K_SPACE:
                        self.game.player_hit()
                    elif event.key == pygame.K_s or event.key == pygame.K_RETURN:
                        self.game.player_stand()
        
        return True
    
    def run(self):
        """Loop principal del juego"""
        running = True
        
        while running:
            running = self.handle_events()
            
            # Actualizar turno del dealer
            if self.game.game_state == "DEALER_TURN":
                self.game.dealer_turn(time.time())
            
            # Dibujar
            self.draw_table()
            
            if self.game.game_state == "BETTING":
                self.draw_betting_screen()
            else:
                self.draw_game_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()