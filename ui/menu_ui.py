import pygame
from constants import *
from ui.utils import draw_text, draw_pill_button, draw_logo, draw_speaker, draw_icon
from logic.game_engine import GameMode

class MenuRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        # Mouse position for hover detection
        mouse_pos = pygame.mouse.get_pos()
        draw_logo(self.screen.screen, WIDTH // 2, 100, self.screen.title_font)
        
        #  Settings Rows
        label_x = 300
        btn_start_x = 310
        row_y = 305
        spacing = 80
        icon_x = label_x + 10

        # Players
        draw_text(self.screen.screen, "Players", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        pve_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 90, 60)
        pvp_rect = pygame.Rect(btn_start_x + 120, row_y - 30, 90, 60)
        draw_pill_button(self.screen.screen, "PVE", pve_rect.x, pve_rect.y, pve_rect.w, pve_rect.h, self.screen.font, self.screen.mode == GameMode.PVE, is_hovered=pve_rect.collidepoint(mouse_pos))
        draw_pill_button(self.screen.screen, "PVP", pvp_rect.x, pvp_rect.y, pvp_rect.w, pvp_rect.h, self.screen.font, self.screen.mode == GameMode.PVP, is_hovered=pvp_rect.collidepoint(mouse_pos))
        
        # Difficulty
        row_y += spacing
        is_diff_disabled = (self.screen.mode == GameMode.PVP)
        diff_color = UI_DISABLED_GRAY if is_diff_disabled else DARK_TEAL
        draw_text(self.screen.screen, "Difficulty", label_x - 10, row_y, self.screen.label_font, diff_color, align="right")        
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        diff_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 190, 60)
        diff_bg = UI_DISABLED_GRAY if is_diff_disabled else RED
        # Brighten on hover
        if not is_diff_disabled and diff_rect.collidepoint(mouse_pos):
            diff_bg = tuple(min(255, c + 30) for c in diff_bg)
        pygame.draw.rect(self.screen.screen, diff_bg, diff_rect, border_radius=20)
        draw_text(self.screen.screen, self.screen.difficulty.capitalize(), diff_rect.centerx - 20, diff_rect.centery, self.screen.font, WHITE)
        if "dropdown" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["dropdown"], btn_start_x + 160 + 20 , row_y, center=True)
        
        #  Board
        row_y += spacing
        draw_text(self.screen.screen, "Board", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        board_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 190, 60)
        board_bg = RED
        if board_rect.collidepoint(mouse_pos):
            board_bg = tuple(min(255, c + 30) for c in board_bg)
        pygame.draw.rect(self.screen.screen, board_bg, board_rect, border_radius=20)
        draw_text(self.screen.screen, self.screen.board_size_name, board_rect.centerx - 20, board_rect.centery, self.screen.font, WHITE)
        if "dropdown" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["dropdown"], btn_start_x + 160 + 20 , row_y, center=True)

        # Custom Indicators
        if self.screen.board_size_name == "Custom":
            rows, cols = self.screen.board_size
            r_rect = pygame.Rect(btn_start_x + 220, row_y - 30, 60, 60)
            c_rect = pygame.Rect(btn_start_x + 300, row_y - 30, 60, 60)
            
            r_bg = RED
            if r_rect.collidepoint(mouse_pos): r_bg = tuple(min(255, c + 30) for c in r_bg)
            pygame.draw.circle(self.screen.screen, r_bg, r_rect.center, 30)
            
            c_bg = RED
            if c_rect.collidepoint(mouse_pos): c_bg = tuple(min(255, c + 30) for c in c_bg)
            pygame.draw.circle(self.screen.screen, c_bg, c_rect.center, 30)
            
            draw_text(self.screen.screen, str(rows), r_rect.centerx, r_rect.centery, self.screen.font, WHITE)
            draw_text(self.screen.screen, "x", btn_start_x + 290, row_y, self.screen.small_font, DARK_TEAL)
            draw_text(self.screen.screen, str(cols), c_rect.centerx, c_rect.centery, self.screen.font, WHITE)
        
        # Quick Game
        row_y += spacing
        draw_text(self.screen.screen, "Quick Game", label_x - 10, row_y, self.screen.label_font, DARK_TEAL, align="right")
        draw_icon(self.screen.screen, self.screen.icons["arrow"], icon_x - 15, row_y - 16, center=False)
        
        on_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 90, 60)
        off_rect = pygame.Rect(btn_start_x + 120, row_y - 30, 90, 60)
        draw_pill_button(self.screen.screen, "On", on_rect.x, on_rect.y, on_rect.w, on_rect.h, self.screen.font, self.screen.is_quickplay, is_hovered=on_rect.collidepoint(mouse_pos))
        draw_pill_button(self.screen.screen, "Off", off_rect.x, off_rect.y, off_rect.w, off_rect.h, self.screen.font, not self.screen.is_quickplay, is_hovered=off_rect.collidepoint(mouse_pos))
        
        # SAVE Button (3D Effect with Hover)
        save_btn_w, save_btn_h = 240, 100
        save_rect = pygame.Rect(WIDTH//2 - save_btn_w//2, 660, save_btn_w, save_btn_h)
        is_save_hovered = save_rect.collidepoint(mouse_pos)
        
        shadow_offset = 8 if is_save_hovered else 6
        lift = -2 if is_save_hovered else 0
        
        # Shadow
        pygame.draw.rect(self.screen.screen, DARK_TEAL, (save_rect.x, save_rect.y + shadow_offset, save_rect.w, save_rect.h), border_radius=25)
        # Button
        s_bg = tuple(min(255, c + 20) for c in RED) if is_save_hovered else RED
        save_draw_rect = pygame.Rect(save_rect.x, save_rect.y + lift, save_rect.w, save_rect.h)
        pygame.draw.rect(self.screen.screen, s_bg, save_draw_rect, border_radius=25)
        pygame.draw.rect(self.screen.screen, WHITE, save_draw_rect, 2, border_radius=25)
        draw_text(self.screen.screen, "SAVE", save_draw_rect.centerx, save_draw_rect.centery, self.screen.play_font, WHITE)
        
        # Help Button
        help_rect = pygame.Rect(WIDTH - 90, HEIGHT - 90, 60, 60)
        is_help_hovered = help_rect.collidepoint(mouse_pos)
        h_radius = 33 if is_help_hovered else 30
        h_bg = tuple(min(255, c + 30) for c in CYAN) if is_help_hovered else CYAN
        pygame.draw.circle(self.screen.screen, h_bg, help_rect.center, h_radius)
        draw_text(self.screen.screen, "?", help_rect.centerx, help_rect.centery, self.screen.font, WHITE)

        # Speaker Button
        speaker_rect = pygame.Rect(30, HEIGHT - 90, 60, 60)
        hover_speaker = speaker_rect.collidepoint(mouse_pos)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on, hover_speaker)

        if self.screen.show_dropdown:
            self.draw_dropdown()
        
        if self.screen.show_diff_dropdown:
            self.draw_diff_dropdown()
        
        if self.screen.show_help:
            self.draw_help_overlay()

        if self.screen.choosing_custom_row or self.screen.choosing_custom_col:
            self.draw_number_picker()

    # Vẽ bảng số để chọn hàng/cột
    def draw_number_picker(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((50, 80, 80))
        self.screen.screen.blit(overlay, (0, 0))
        
        picker_x = WIDTH // 2 - 150
        picker_y = HEIGHT // 2 - 150
        
        panel_rect = pygame.Rect(picker_x - 20, picker_y - 80, 340, 400) # 20, 80, 340: rộng, 440: cao
        pygame.draw.rect(self.screen.screen, BG_COLOR, panel_rect, border_radius=20)
        title = "Select Rows" if self.screen.choosing_custom_row else "Select Columns"
        draw_text(self.screen.screen, title, WIDTH // 2, picker_y - 45, self.screen.label_font, DARK_TEAL)

        for i in range(19): # Numbers 2 to 20
            num = i + 2
            row, col = i // 5, i % 5
            btn_size = 60
            btn_rect = pygame.Rect(picker_x + col * btn_size, picker_y + row * btn_size, btn_size, btn_size)
            pygame.draw.rect(self.screen.screen, RED, btn_rect)
            pygame.draw.rect(self.screen.screen, WHITE, btn_rect, 1) # Thin white border
            draw_text(self.screen.screen, str(num), btn_rect.centerx, btn_rect.centery, self.screen.font, WHITE)
            
    # Dropdown của Difficulty
    def draw_diff_dropdown(self):
        mouse_pos = pygame.mouse.get_pos()
        options = ["Easy", "Medium", "Hard"]
        start_y = 430
        btn_start_x = 310
        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_start_x + 20, start_y + i * 60, 190, 60)
            bg = RED
            if rect.collidepoint(mouse_pos): bg = tuple(min(255, c + 30) for c in bg)
            pygame.draw.rect(self.screen.screen, bg, rect)
            pygame.draw.line(self.screen.screen, WHITE, (btn_start_x + 20, rect.bottom), (btn_start_x + 210, rect.bottom), 1)
            draw_text(self.screen.screen, opt, rect.centerx, rect.centery, self.screen.font, WHITE)

    # Dropdown của Board
    def draw_dropdown(self):
        mouse_pos = pygame.mouse.get_pos()
        options = ["Small", "Medium", "Large", "Custom"]
        start_y = 500
        btn_start_x = 310
        
        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_start_x + 20, start_y + i * 60, 190, 60)
            bg = RED
            if rect.collidepoint(mouse_pos): bg = tuple(min(255, c + 30) for c in bg)
            pygame.draw.rect(self.screen.screen, bg, rect)
            pygame.draw.line(self.screen.screen, WHITE, (btn_start_x + 20, rect.bottom), (btn_start_x + 210, rect.bottom), 1)
            draw_text(self.screen.screen, opt, rect.centerx, rect.centery, self.screen.font, WHITE)
    
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
        mouse_pos = pygame.mouse.get_pos()
        close_y = 620
        close_rect = pygame.Rect(WIDTH//2 - 30, close_y - 30, 60, 60)
        is_close_hovered = close_rect.collidepoint(mouse_pos)
        c_radius = 33 if is_close_hovered else 30
        c_bg = tuple(min(255, c + 30) for c in CYAN) if is_close_hovered else CYAN
        
        pygame.draw.circle(self.screen.screen, c_bg, (WIDTH//2, close_y), c_radius)
        if "close" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["close"], WIDTH//2, close_y, center=True)
        else:
            draw_text(self.screen.screen, "✕", WIDTH//2, close_y, self.screen.font, WHITE)
