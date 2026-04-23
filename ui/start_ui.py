import pygame
from constants import *
from ui.utils import draw_text, draw_logo, draw_speaker, draw_modern_background

class StartRenderer:
    def __init__(self, screen):
        self.screen = screen

    def _draw_button(self, text, rect, base_color=CYAN, is_hovered=False):
        # Modern 3D Button with smoother shadows and highlights
        shadow_offset = 10 if is_hovered else 6
        lift_offset = -4 if is_hovered else 0
        
        draw_rect = rect.copy()
        draw_rect.y += lift_offset
        
        # Outer Shadow (Glow-like)
        shadow_rect = rect.copy()
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen.screen, DARK_TEAL, shadow_rect, border_radius=30)
        
        # Adjust color for hover
        color = tuple(min(255, c + 40) for c in base_color) if is_hovered else base_color
        
        # Main button body
        pygame.draw.rect(self.screen.screen, color, draw_rect, border_radius=30)
        # Top highlight line
        pygame.draw.line(self.screen.screen, WHITE, (draw_rect.left + 20, draw_rect.top + 4), (draw_rect.right - 20, draw_rect.top + 4), 2)
        
        # Inner light border
        pygame.draw.rect(self.screen.screen, WHITE, draw_rect, 2, border_radius=30)
        
        # Text with shadow
        draw_text(self.screen.screen, text, draw_rect.centerx, draw_rect.centery, self.screen.label_font, WHITE)

    def draw(self):
        # Modern Background with grid dots
        draw_modern_background(self.screen.screen)
        
        # Mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()
        
        # Logo
        draw_logo(self.screen.screen, WIDTH // 2, 100, self.screen.title_font)
        
        # Buttons Setup
        btn_w, btn_h = 320, 90
        start_x = WIDTH // 2 - btn_w // 2
        start_y = 280
        spacing = 120
        
        self.start_game_rect = pygame.Rect(start_x, start_y, btn_w, btn_h)
        hover_start = self.start_game_rect.collidepoint(mouse_pos)
        self._draw_button("PLAY GAME", self.start_game_rect, RED, hover_start)
        
        self.settings_rect = pygame.Rect(start_x, start_y + spacing, btn_w, btn_h)
        hover_settings = self.settings_rect.collidepoint(mouse_pos)
        self._draw_button("SETTINGS", self.settings_rect, CYAN, hover_settings)
        
        self.exit_rect = pygame.Rect(start_x, start_y + 2 * spacing, btn_w, btn_h)
        hover_exit = self.exit_rect.collidepoint(mouse_pos)
        self._draw_button("QUIT GAME", self.exit_rect, CYAN, hover_exit)
        
        # Speaker Button (Bottom Left)
        self.speaker_rect = pygame.Rect(30, HEIGHT - 90, 60, 60)
        hover_speaker = self.speaker_rect.collidepoint(mouse_pos)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on, hover_speaker)
