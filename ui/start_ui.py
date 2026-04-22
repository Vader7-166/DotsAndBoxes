import pygame
from constants import *
from ui.utils import draw_text, draw_logo, draw_speaker

class StartRenderer:
    def __init__(self, screen):
        self.screen = screen

    def _draw_button(self, text, rect, base_color=CYAN, is_hovered=False):
        # Apply hover effects: move shadow and button slightly for a "lifted" feel
        shadow_offset = 8 if is_hovered else 6
        lift_offset = -2 if is_hovered else 0
        
        draw_rect = rect.copy()
        draw_rect.y += lift_offset
        
        # Shadow
        shadow_rect = rect.copy()
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen.screen, DARK_TEAL, shadow_rect, border_radius=25)
        
        # Adjust color for hover
        color = tuple(min(255, c + 30) for c in base_color) if is_hovered else base_color
        
        # Main button
        pygame.draw.rect(self.screen.screen, color, draw_rect, border_radius=25)
        
        # Inner light border
        pygame.draw.rect(self.screen.screen, WHITE, draw_rect, 2, border_radius=25)
        
        # Text
        draw_text(self.screen.screen, text, draw_rect.centerx, draw_rect.centery, self.screen.label_font, WHITE)

    def draw(self):
        # Background
        self.screen.screen.fill(BG_COLOR)
        
        # Mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()
        
        # Logo
        draw_logo(self.screen.screen, WIDTH // 2, 100, self.screen.title_font)
        
        # Buttons Setup
        btn_w, btn_h = 320, 90
        start_x = WIDTH // 2 - btn_w // 2
        start_y = 280
        spacing = 120
        
        # Start Game Button
        self.start_game_rect = pygame.Rect(start_x, start_y, btn_w, btn_h)
        hover_start = self.start_game_rect.collidepoint(mouse_pos)
        self._draw_button("START GAME", self.start_game_rect, RED, hover_start)
        
        # Settings Button
        self.settings_rect = pygame.Rect(start_x, start_y + spacing, btn_w, btn_h)
        hover_settings = self.settings_rect.collidepoint(mouse_pos)
        self._draw_button("SETTINGS", self.settings_rect, CYAN, hover_settings)
        
        # Exit Button
        self.exit_rect = pygame.Rect(start_x, start_y + 2 * spacing, btn_w, btn_h)
        hover_exit = self.exit_rect.collidepoint(mouse_pos)
        self._draw_button("EXIT", self.exit_rect, CYAN, hover_exit)
        
        # Speaker Button (Bottom Left)
        self.speaker_rect = pygame.Rect(30, HEIGHT - 90, 60, 60)
        hover_speaker = self.speaker_rect.collidepoint(mouse_pos)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on, hover_speaker)
