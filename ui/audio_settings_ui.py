import pygame
from constants import *
from ui.utils import draw_text, draw_pill_button, draw_icon

class AudioSettingsUI:
    def __init__(self, screen_instance, audio_manager):
        self.screen_instance = screen_instance
        self.audio_manager = audio_manager
        self.dragging_music = False
        self.dragging_sfx = False
        
        # Slider positions
        self.slider_x = 300
        self.slider_w = 350
        self.music_y = 300
        self.sfx_y = 420
        self.mute_y = 540

    def draw(self):
        screen = self.screen_instance.screen
        
        # Title
        draw_text(screen, "AUDIO SETTINGS", WIDTH // 2, 100, self.screen_instance.title_font, DARK_TEAL)
        
        # Music Volume Slider
        draw_text(screen, "Music", 150, self.music_y, self.screen_instance.label_font, DARK_TEAL, align="left")
        self._draw_slider(self.slider_x, self.music_y, self.slider_w, self.audio_manager.bgm_volume)
        draw_text(screen, f"{int(self.audio_manager.bgm_volume * 100)}%", self.slider_x + self.slider_w + 50, self.music_y, self.screen_instance.font, DARK_TEAL)

        # SFX Volume Slider
        draw_text(screen, "SFX", 150, self.sfx_y, self.screen_instance.label_font, DARK_TEAL, align="left")
        self._draw_slider(self.slider_x, self.sfx_y, self.slider_w, self.audio_manager.sfx_volume)
        draw_text(screen, f"{int(self.audio_manager.sfx_volume * 100)}%", self.slider_x + self.slider_w + 50, self.sfx_y, self.screen_instance.font, DARK_TEAL)

        # Mute All Toggle
        draw_text(screen, "Mute All", 150, self.mute_y, self.screen_instance.label_font, DARK_TEAL, align="left")
        mute_text = "ON" if self.audio_manager.is_muted else "OFF"
        draw_pill_button(screen, mute_text, self.slider_x, self.mute_y - 25, 100, 50, self.screen_instance.font, self.audio_manager.is_muted)

        # Back Button
        back_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
        pygame.draw.rect(screen, RED, back_rect, border_radius=20)
        draw_text(screen, "BACK", WIDTH // 2, HEIGHT - 70, self.screen_instance.font, WHITE)

    def _draw_slider(self, x, y, w, volume):
        screen = self.screen_instance.screen
        # Track
        pygame.draw.rect(screen, GRAY, (x, y - 5, w, 10), border_radius=5)
        # Active track
        pygame.draw.rect(screen, CYAN, (x, y - 5, int(w * volume), 10), border_radius=5)
        # Handle
        handle_x = x + int(w * volume)
        pygame.draw.circle(screen, WHITE, (handle_x, y), 15)
        pygame.draw.circle(screen, DARK_TEAL, (handle_x, y), 15, 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            # Back Button
            if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT - 100 <= y <= HEIGHT - 40:
                self.screen_instance.state = self.screen_instance.previous_state
                return True
                
            # Mute Toggle
            if self.slider_x <= x <= self.slider_x + 100 and self.mute_y - 25 <= y <= self.mute_y + 25:
                self.audio_manager.toggle_mute()
                return True

            # Sliders
            if self.slider_x - 15 <= x <= self.slider_x + self.slider_w + 15:
                if self.music_y - 20 <= y <= self.music_y + 20:
                    self.dragging_music = True
                    self._update_volume_from_mouse(x, 'music')
                    return True
                elif self.sfx_y - 20 <= y <= self.sfx_y + 20:
                    self.dragging_sfx = True
                    self._update_volume_from_mouse(x, 'sfx')
                    return True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_music = False
            self.dragging_sfx = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_music:
                self._update_volume_from_mouse(event.pos[0], 'music')
            elif self.dragging_sfx:
                self._update_volume_from_mouse(event.pos[0], 'sfx')

    def _update_volume_from_mouse(self, mouse_x, type):
        volume = max(0.0, min(1.0, (mouse_x - self.slider_x) / self.slider_w))
        if type == 'music':
            self.audio_manager.set_bgm_volume(volume)
        else:
            self.audio_manager.set_sfx_volume(volume)
