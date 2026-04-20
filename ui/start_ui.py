import pygame
from constants import *
from ui.utils import draw_text, draw_logo, draw_speaker

class StartRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        # Background
        self.screen.screen.fill(BG_COLOR)
        
        # Logo
        draw_logo(self.screen.screen, WIDTH // 2, 150, self.screen.title_font)
        
        # Buttons Setup
        btn_w, btn_h = 300, 80
        start_x = WIDTH // 2 - btn_w // 2
        start_y = 300
        spacing = 100
        
        # Start Game Button
        self.start_game_rect = pygame.Rect(start_x, start_y, btn_w, btn_h)
        self._draw_button("START GAME", self.start_game_rect)
        
        # Settings Button
        self.settings_rect = pygame.Rect(start_x, start_y + spacing, btn_w, btn_h)
        self._draw_button("SETTINGS", self.settings_rect)
        
        # Exit Button
        self.exit_rect = pygame.Rect(start_x, start_y + 2 * spacing, btn_w, btn_h)
        self._draw_button("EXIT", self.exit_rect)
        
        # Speaker Button (Bottom Left)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on)

    def _draw_button(self, text, rect):
        # Using DARK_TEAL for consistency with established UI
        pygame.draw.rect(self.screen.screen, DARK_TEAL, rect, 2, border_radius=15)
        draw_text(self.screen.screen, text, rect.centerx, rect.centery, self.screen.label_font, DARK_TEAL)
