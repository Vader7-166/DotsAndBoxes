import pygame
from constants import *
from ui.utils import draw_text, draw_pill_button, draw_logo, draw_speaker, draw_icon
from logic.game_engine import GameMode

class MenuRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        draw_logo(self.screen.screen, WIDTH // 2, 100, self.screen.title_font)
        
        #  Settings Rows
        label_x = 300
        btn_start_x = 310
        row_y = 305
        spacing = 80
        icon_x = label_x + 10
        icon_y = row_y - 16

        # Players
        draw_text(self.screen.screen, "Players", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        draw_pill_button(self.screen.screen, "PVE", btn_start_x + 20, row_y - 30, 90, 60, self.screen.font, self.screen.mode == GameMode.PVE)
        draw_pill_button(self.screen.screen, "PVP", btn_start_x + 100 + 20, row_y - 30, 90, 60, self.screen.font, self.screen.mode == GameMode.PVP)
        
        # Difficulty
        row_y += spacing
        is_diff_disabled = (self.screen.mode == GameMode.PVP)
        diff_color = UI_DISABLED_GRAY if is_diff_disabled else DARK_TEAL
        draw_text(self.screen.screen, "Difficulty", label_x - 10, row_y, self.screen.label_font, diff_color, align="right")        
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        diff_bg = UI_DISABLED_GRAY if is_diff_disabled else RED
        pygame.draw.rect(self.screen.screen, diff_bg, (btn_start_x + 20, row_y - 30, 190, 60), border_radius=20)
        draw_text(self.screen.screen, self.screen.difficulty.capitalize(), btn_start_x + 75 + 20, row_y, self.screen.font, WHITE)
        if "dropdown" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["dropdown"], btn_start_x + 160 + 20 , row_y, center=True)
        
        #  Board
        row_y += spacing
        draw_text(self.screen.screen, "Board", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        pygame.draw.rect(self.screen.screen, RED, (btn_start_x + 20, row_y - 30, 190, 60), border_radius=20)
        draw_text(self.screen.screen, self.screen.board_size_name, btn_start_x + 75 , row_y, self.screen.font, WHITE)
        if "dropdown" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["dropdown"], btn_start_x + 160 + 20 , row_y, center=True)
        
        # Quick Game
        row_y += spacing
        draw_text(self.screen.screen, "Quick Game", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        draw_pill_button(self.screen.screen, "On", btn_start_x + 20, row_y - 30, 90, 60, self.screen.font, self.screen.is_quickplay)
        draw_pill_button(self.screen.screen, "Off", btn_start_x + 100 + 20, row_y - 30, 90, 60, self.screen.font, not self.screen.is_quickplay)
        
        # SAVE Button
        play_rect = pygame.Rect(WIDTH//2 - 120, 660, 240, 100)
        pygame.draw.rect(self.screen.screen, (220, 240, 240), (play_rect.x+2, play_rect.y+8, play_rect.w, play_rect.h), border_radius=25)
        pygame.draw.rect(self.screen.screen, RED, (play_rect.x, play_rect.y+4, play_rect.w, play_rect.h), border_radius=25)
        pygame.draw.rect(self.screen.screen, WHITE, play_rect, border_radius=25)
        draw_text(self.screen.screen, "SAVE", WIDTH//2, 710, self.screen.play_font, RED)
        
        # Help Button
        help_rect = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
        pygame.draw.circle(self.screen.screen, CYAN, help_rect.center, 30)
        draw_text(self.screen.screen, "?", help_rect.centerx, help_rect.centery, self.screen.font, WHITE)

        # Speaker Button (Bottom Left)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on)

        if self.screen.show_dropdown:
            self.draw_dropdown()
        
        if self.screen.show_diff_dropdown:
            self.draw_diff_dropdown()
        
        if self.screen.show_help:
            self.draw_help_overlay()
    # Dropdown của Difficulty
    def draw_diff_dropdown(self):
        options = ["Easy", "Medium", "Hard"]
        start_y = 430
        btn_start_x = 310
        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_start_x + 20, start_y + i * 60, 190, 60)
            pygame.draw.rect(self.screen.screen, RED, rect)
            pygame.draw.line(self.screen.screen, WHITE, (btn_start_x + 20, rect.bottom), (btn_start_x + 210, rect.bottom), 1)
            draw_text(self.screen.screen, opt, btn_start_x + 95 + 20, rect.centery, self.screen.font, WHITE)
    # Dropdown của Board
    def draw_dropdown(self):
        options = ["Small", "Medium", "Large", "Custom"]
        start_y = 500
        btn_start_x = 310
        
        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_start_x + 20, start_y + i * 60, 190, 60)
            pygame.draw.rect(self.screen.screen, RED, rect)
            pygame.draw.line(self.screen.screen, WHITE, (btn_start_x, rect.bottom), (btn_start_x + 190, rect.bottom), 1)
            draw_text(self.screen.screen, opt, btn_start_x + 95, rect.centery, self.screen.font, WHITE)
    
    def draw_help_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((50, 80, 80))
        self.screen.screen.blit(overlay, (0, 0))
        
        #Kích thước của panel hiện lên
        panel_rect = pygame.Rect(WIDTH//2 - 180, 200, 360, 480)
        pygame.draw.rect(self.screen.screen, BG_COLOR, panel_rect, border_radius=20)
        
        help_text = [
            "Take turns drawing a line to",
            "connect two dots. If your line",
            "closes up a box, you score a point",
            "and take another turn. The player",
            "with the most boxes after all the",
            "lines are drawn wins the game."
        ]
        
        y = 240
        for line in help_text:
            draw_text(self.screen.screen, line, WIDTH//2, y, self.screen.small_font, DARK_TEAL)
            y += 28
            
        box_y = y + 40
        bx, by = WIDTH//2 - 25, box_y
        bs = 50
        pygame.draw.line(self.screen.screen, DARK_TEAL, (bx, by), (bx + bs, by), 6)
        pygame.draw.line(self.screen.screen, DARK_TEAL, (bx, by + bs), (bx + bs, by + bs), 6)
        pygame.draw.line(self.screen.screen, DARK_TEAL, (bx, by), (bx, by + bs), 6)
        pygame.draw.line(self.screen.screen, DARK_TEAL, (bx + bs, by), (bx + bs, by + bs), 6)
        for dx in [0, bs]:
            for dy in [0, bs]:
                pygame.draw.circle(self.screen.screen, WHITE, (bx + dx, by + dy), 8)
                pygame.draw.circle(self.screen.screen, DARK_TEAL, (bx + dx, by + dy), 8, 2)

        draw_text(self.screen.screen, "Tip: Try Quick Game to get to the", WIDTH//2, box_y + 90, self.screen.small_font, DARK_TEAL)
        draw_text(self.screen.screen, "scoring sooner.", WIDTH//2, box_y + 115, self.screen.small_font, DARK_TEAL)
        
        #Nút đóng X
        close_y = 620
        pygame.draw.circle(self.screen.screen, CYAN, (WIDTH//2, close_y), 30)
        if "close" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["close"], WIDTH//2, close_y, center=True)
        else:
            draw_text(self.screen.screen, "✕", WIDTH//2, close_y, self.screen.font, WHITE)
