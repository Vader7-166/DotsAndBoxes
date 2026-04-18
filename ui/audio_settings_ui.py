import pygame
from constants import *

class AudioSettingsUI:
    def __init__(self, screen_instance, audio_manager):
        self.screen_instance = screen_instance
        self.audio_manager = audio_manager

    def draw(self):
        self.screen_instance._draw_text("AUDIO SETTINGS", WIDTH//2, 80, self.screen_instance.title_font, BLACK)
        
        label_x = 100
        slider_x = 300
        slider_w = 400
        
        # BGM Volume
        self.screen_instance._draw_text("Music Volume", label_x, 245, self.screen_instance.font, align="left")
        self._draw_volume_slider(slider_x, 220, slider_w, 50, self.audio_manager.bgm_volume)
        self.screen_instance._draw_text(f"{int(self.audio_manager.bgm_volume * 100)}%", slider_x + slider_w + 50, 245, self.screen_instance.small_font, align="left")
        
        # SFX Volume
        self.screen_instance._draw_text("SFX Volume", label_x, 345, self.screen_instance.font, align="left")
        self._draw_volume_slider(slider_x, 320, slider_w, 50, self.audio_manager.sfx_volume)
        self.screen_instance._draw_text(f"{int(self.audio_manager.sfx_volume * 100)}%", slider_x + slider_w + 50, 345, self.screen_instance.small_font, align="left")
        
        # Mute All
        self.screen_instance._draw_text("Mute All", label_x, 445, self.screen_instance.font, align="left")
        mute_text = "MUTED" if self.audio_manager.is_muted else "SOUND ON"
        self.screen_instance._draw_button(mute_text, slider_x, 420, 200, 50, self.audio_manager.is_muted)
        
        self.screen_instance._draw_button("Back to Settings", 20, HEIGHT - 80, 250, 50)

    def _draw_volume_slider(self, x, y, w, h, volume):
        # Draw track
        pygame.draw.rect(self.screen_instance.screen, GRAY, (x, y + h//2 - 2, w, 4))
        
        # Draw handle
        handle_x = x + int(volume * w)
        pygame.draw.circle(self.screen_instance.screen, BLACK, (handle_x, y + h//2), 10)
        
        if pygame.Rect(x, y, w, h).collidepoint(self.screen_instance.mouse_pos):
            pygame.draw.circle(self.screen_instance.screen, HOVER_COLOR, (handle_x, y + h//2), 12, 2)

    def handle_click(self, x, y):
        # Back to Settings
        if 20 <= x <= 270 and HEIGHT - 80 <= y <= HEIGHT - 30:
            self.screen_instance.state = 'SETTINGS'
            return True
            
        # Volume Sliders and Mute
        slider_x = 300
        slider_w = 400
        
        # Music Slider
        if 220 <= y <= 270 and slider_x <= x <= slider_x + slider_w:
            new_vol = (x - slider_x) / slider_w
            self.audio_manager.set_bgm_volume(new_vol)
            return True
            
        # SFX Slider
        if 320 <= y <= 370 and slider_x <= x <= slider_x + slider_w:
            new_vol = (x - slider_x) / slider_w
            self.audio_manager.set_sfx_volume(new_vol)
            return True
            
        # Mute Toggle
        if 420 <= y <= 470 and slider_x <= x <= slider_x + 200:
            self.audio_manager.toggle_mute()
            return True
            
        return False
