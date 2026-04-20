import pygame
from constants import *
from ui.utils import draw_text, draw_logo, draw_speaker

class StartRenderer:
    def __init__(self, screen):
        self.screen = screen

    def _draw_button(self, text, rect, base_color=CYAN):
        # Draw shadow
        shadow_rect = rect.copy()
        shadow_rect.y += 6
        pygame.draw.rect(self.screen.screen, DARK_TEAL, shadow_rect, border_radius=25)
        
        # Draw main button
        pygame.draw.rect(self.screen.screen, base_color, rect, border_radius=25)
        
        # Draw inner light border for depth
        inner_rect = rect.inflate(-4, -4)
        pygame.draw.rect(self.screen.screen, WHITE, rect, 2, border_radius=25)
        
        # Text
        draw_text(self.screen.screen, text, rect.centerx, rect.centery, self.screen.label_font, WHITE)

    def draw(self):
        # Background
        self.screen.screen.fill(BG_COLOR)
        
        # Logo
        draw_logo(self.screen.screen, WIDTH // 2, 100, self.screen.title_font)
        
        # Buttons Setup
        btn_w, btn_h = 320, 90
        start_x = WIDTH // 2 - btn_w // 2
        start_y = 280
        spacing = 120
        
        # Start Game Button (RED for emphasis)
        self.start_game_rect = pygame.Rect(start_x, start_y, btn_w, btn_h)
        self._draw_button("START GAME", self.start_game_rect, RED)
        
        # Settings Button
        self.settings_rect = pygame.Rect(start_x, start_y + spacing, btn_w, btn_h)
        self._draw_button("SETTING", self.settings_rect, CYAN)
        
        # Exit Button
        self.exit_rect = pygame.Rect(start_x, start_y + 2 * spacing, btn_w, btn_h)
        self._draw_button("EXIT", self.exit_rect, CYAN)
        
        # Speaker Button (Bottom Left)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on)
