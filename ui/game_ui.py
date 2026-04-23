from constants import P2_LIGHT_COLOR
import pygame
import time
import math
from constants import *
from ui.utils import draw_text, draw_speaker, draw_icon, draw_glow_line
from logic.game_engine import GameState, GameMode

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self):
        board = self.screen.engine.board
        rows, cols = self.screen.board_size
        
        # HUD: Top Score Bar
        p1_center = (60, 60)
        pygame.draw.circle(self.screen.screen, CYAN, p1_center, 40)
        if self.screen.engine.current_player == 1:
            # Active indicator: Thick CYAN ring
            pygame.draw.circle(self.screen.screen, CYAN, p1_center, 48, 5)
        
        if "user" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["user"], p1_center[0], p1_center[1], center=True)
        else:
            draw_text(self.screen.screen, "P1", p1_center[0], p1_center[1], self.screen.font, WHITE)
        # Score P1
        pygame.draw.circle(self.screen.screen, P1_LIGHT_COLOR, (120, 60), 25)
        draw_text(self.screen.screen, str(board.get_score(1)), 120, 60, self.screen.font, DARK_TEAL)
        
        p2_center = (WIDTH - 60, 60)
        pygame.draw.circle(self.screen.screen, RED, p2_center, 40)
        if self.screen.engine.current_player == 2:
            # Active indicator: Thick RED ring
            pygame.draw.circle(self.screen.screen, RED, p2_center, 48, 5)
            
        p2_icon_key = "user2" if self.screen.mode == GameMode.PVP else "robot"
        if p2_icon_key in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons[p2_icon_key], p2_center[0], p2_center[1], center=True)
        else:
            p2_label_icon = "P2" if self.screen.mode == GameMode.PVP else "AI"
            draw_text(self.screen.screen, p2_label_icon, p2_center[0], p2_center[1], self.screen.font, WHITE)
        # Score P2
        pygame.draw.circle(self.screen.screen, P2_LIGHT_COLOR, (WIDTH - 120, 60), 25)
        draw_text(self.screen.screen, str(board.get_score(2)), WIDTH - 120, 60, self.screen.font, DARK_TEAL)

        if self.screen.engine.is_quickplay and self.screen.engine.turn_start_time:
            time_left = max(0, int(self.screen.engine.turn_time_limit - (time.time() - self.screen.engine.turn_start_time)))
            color = RED if time_left <= 3 else DARK_TEAL
            draw_text(self.screen.screen, f"{time_left:02d}", WIDTH // 2, 60, self.screen.play_font, color)

        # Boxes
        for r in range(rows):
            for c in range(cols):
                owner = board.boxes[r][c]
                if owner != 0:
                    color = P1_LIGHT_COLOR if owner == 1 else P2_LIGHT_COLOR
                    rect = pygame.Rect(
                        self.screen.margin_x + c * self.screen.square_size,
                        self.screen.margin_y + r * self.screen.square_size,
                        self.screen.square_size,
                        self.screen.square_size
                    )
                    pygame.draw.rect(self.screen.screen, color, rect)

        # Hovered Edge (Hiệu ứng nối từ điểm này sang điểm kia mượt mà hơn)
        if self.screen.hovered_edge and self.screen.engine.current_player == 1 and not self.screen.is_dragging:
            d, r, c = self.screen.hovered_edge
            hover_color = P1_LIGHT_COLOR
            
            s = self.screen.square_size
            if d == 'h':
                x1 = self.screen.margin_x + c * s
                x2 = x1 + s
                y = self.screen.margin_y + r * s
                
                # Vẽ một hình con nhộng (capsule) nối chính xác từ TÂM điểm bên trái sang TÂM điểm bên phải
                rect = pygame.Rect(x1, y - HOVER_EDGE_WIDTH//2, 
                                 s, HOVER_EDGE_WIDTH)
                pygame.draw.rect(self.screen.screen, hover_color, rect, border_radius=HOVER_EDGE_WIDTH//2)
                
            else:
                x = self.screen.margin_x + c * s
                y1 = self.screen.margin_y + r * s
                y2 = y1 + s
                
                # Vẽ một hình con nhộng (capsule) nối chính xác từ TÂM điểm bên trên xuống TÂM điểm bên dưới
                rect = pygame.Rect(x - HOVER_EDGE_WIDTH//2, y1,
                                 HOVER_EDGE_WIDTH, s)
                pygame.draw.rect(self.screen.screen, hover_color, rect, border_radius=HOVER_EDGE_WIDTH//2)

        # Edges (Vẽ cạnh chính thức)
        for r in range(rows + 1):
            for c in range(cols):
                if board.h_edges[r][c]:
                    owner = board.h_edge_owners[r][c]
                    is_last = self.screen.last_move == ('h', r, c)
                    
                    s = self.screen.square_size
                    x1 = self.screen.margin_x + c * s
                    x2 = x1 + s
                    y = self.screen.margin_y + r * s
                    
                    if is_last:
                        # Nét cuối cùng: Sáng rực và dày hơn
                        width = EDGE_WIDTH + 6
                        color = LAST_MOVE_COLOR
                        draw_glow_line(self.screen.screen, color, (x1, y), (x2, y), width, glow_radius=5)
                    else:
                        # Các nét cũ: Chung một màu trung tính
                        width = EDGE_WIDTH
                        color = COMPLETED_EDGE_COLOR
                        rect = pygame.Rect(x1, y - width//2, s, width)
                        pygame.draw.rect(self.screen.screen, color, rect, border_radius=width//2)

        for r in range(rows):
            for c in range(cols + 1):
                if board.v_edges[r][c]:
                    owner = board.v_edge_owners[r][c]
                    is_last = self.screen.last_move == ('v', r, c)
                    
                    s = self.screen.square_size
                    x = self.screen.margin_x + c * s
                    y1 = self.screen.margin_y + r * s
                    y2 = y1 + s
                    
                    if is_last:
                        # Nét cuối cùng: Sáng rực và dày hơn
                        width = EDGE_WIDTH + 6
                        color = LAST_MOVE_COLOR
                        draw_glow_line(self.screen.screen, color, (x, y1), (x, y2), width, glow_radius=5)
                    else:
                        # Các nét cũ: Chung một màu trung tính
                        width = EDGE_WIDTH
                        color = COMPLETED_EDGE_COLOR
                        rect = pygame.Rect(x - width//2, y1, width, s)
                        pygame.draw.rect(self.screen.screen, color, rect, border_radius=width//2)

        # Draw drag line (Hiệu ứng kéo mượt mà với Glow)
        if self.screen.is_dragging and self.screen.drag_start_pos:
            start_r, start_c = self.screen.drag_start_pos
            start_x = self.screen.margin_x + start_c * self.screen.square_size
            start_y = self.screen.margin_y + start_r * self.screen.square_size
            
            end_x, end_y = self.screen.mouse_pos
            
            # Snap to hovered edge dot if valid
            glow_radius = 12
            line_color = P1_LIGHT_COLOR if self.screen.engine.current_player == 1 else P2_LIGHT_COLOR
            
            if self.screen.hovered_edge:
                d, r, c = self.screen.hovered_edge
                if d == 'h':
                    end_x = self.screen.margin_x + (c + 1 if start_c == c else c) * self.screen.square_size
                    end_y = self.screen.margin_y + r * self.screen.square_size
                else:
                    end_x = self.screen.margin_x + c * self.screen.square_size
                    end_y = self.screen.margin_y + (r + 1 if start_r == r else r) * self.screen.square_size
                
                # Khi đã snap, hiệu ứng mạnh hơn và sáng rực rỡ
                glow_radius = 15 + int(math.sin(time.time() * 15) * 5)
            
            draw_glow_line(self.screen.screen, line_color, (start_x, start_y), (end_x, end_y), HOVER_EDGE_WIDTH, glow_radius)

        # Draw Recoil line (Sợi dây chun)
        if self.screen.is_recoiling and self.screen.recoil_data:
            data = self.screen.recoil_data
            elapsed = time.time() - data['time']
            t = elapsed / RECOIL_DURATION
            from ui.utils import ease_out_quad
            t = ease_out_quad(t)
            
            # Start is fixed, end moves towards start
            start = data['start']
            orig_end = data['current_end']
            current_end = orig_end + (start - orig_end) * t
            
            # Fade out alpha
            line_color = P1_LIGHT_COLOR if self.screen.engine.current_player == 1 else P2_LIGHT_COLOR
            # Simple fade
            draw_glow_line(self.screen.screen, line_color, (start.x, start.y), (current_end.x, current_end.y), HOVER_EDGE_WIDTH, 5)


        # Dots (Vẽ đè lên trên Edges và Hovered Edge để nhìn mượt hơn)
        for r in range(rows + 1):
            for c in range(cols + 1):
                dx = self.screen.margin_x + c * self.screen.square_size
                dy = self.screen.margin_y + r * self.screen.square_size
                
                # Hiệu ứng phóng to nhẹ khi dot này đang được chọn để kéo hoặc đang hover
                is_start_dot = self.screen.is_dragging and self.screen.drag_start_pos == (r, c)
                is_hovered_dot = False
                if self.screen.hovered_edge:
                    d, hr, hc = self.screen.hovered_edge
                    if d == 'h':
                        is_hovered_dot = (r == hr and (c == hc or c == hc + 1))
                    else:
                        is_hovered_dot = (c == hc and (r == hr or r == hr + 1))
                
                current_radius = DOT_RADIUS
                dot_color = DARK_TEAL
                if is_start_dot or is_hovered_dot:
                    current_radius = DOT_RADIUS + 4 + int(math.sin(time.time() * 10) * 2)
                    dot_color = RED if self.screen.engine.current_player == 2 else CYAN

                # Đổ bóng nhẹ cho dấu chấm
                pygame.draw.circle(self.screen.screen, (180, 200, 200), (dx, dy + 2), current_radius)
                # Vòng ngoài
                pygame.draw.circle(self.screen.screen, dot_color, (dx, dy), current_radius)
                # Lõi trắng tạo độ bóng 3D
                pygame.draw.circle(self.screen.screen, WHITE, (dx, dy), current_radius - 3)

        # Navigation Bar
        nav_center_x = WIDTH // 2
        nav_y = HEIGHT - 60
        mouse_pos = pygame.mouse.get_pos()
        
        # Home button
        home_pos = (nav_center_x - 55, nav_y)
        home_rect = pygame.Rect(home_pos[0] - 42, home_pos[1] - 42, 84, 84)
        is_home_hovered = home_rect.collidepoint(mouse_pos)
        h_radius = 45 if is_home_hovered else 42
        
        pygame.draw.circle(self.screen.screen, CYAN, home_pos, h_radius)
        if "home" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["home"], home_pos[0], home_pos[1], center=True)
        else:
            draw_text(self.screen.screen, "H", home_pos[0], home_pos[1], self.screen.font, WHITE)
        
        # Restart button
        restart_pos = (nav_center_x + 55, nav_y)
        restart_rect = pygame.Rect(restart_pos[0] - 42, restart_pos[1] - 42, 84, 84)
        is_restart_hovered = restart_rect.collidepoint(mouse_pos)
        r_radius = 45 if is_restart_hovered else 42
        
        pygame.draw.circle(self.screen.screen, CYAN, restart_pos, r_radius)
        if "restart" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["restart"], restart_pos[0], restart_pos[1], center=True)
        else:
            draw_text(self.screen.screen, "R", restart_pos[0], restart_pos[1], self.screen.font, WHITE)
        
        # Help button
        help_pos = (WIDTH - 60, nav_y)
        help_rect = pygame.Rect(help_pos[0] - 30, help_pos[1] - 30, 60, 60)
        is_help_hovered = help_rect.collidepoint(mouse_pos)
        hp_radius = 33 if is_help_hovered else 30
        hp_color = tuple(min(255, c + 30) for c in CYAN) if is_help_hovered else CYAN
        
        pygame.draw.circle(self.screen.screen, hp_color, help_pos, hp_radius)
        draw_text(self.screen.screen, "?", help_pos[0], help_pos[1], self.screen.font, WHITE)

        # Speaker button (Bottom Left)
        speaker_rect = pygame.Rect(30, HEIGHT - 90, 60, 60)
        hover_speaker = speaker_rect.collidepoint(mouse_pos)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on, hover_speaker)

    def draw_game_over(self):
        # Modern Overlay: Darker and smoother
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 30, 30))
        self.screen.screen.blit(overlay, (0, 0))
        
        if self.screen.engine.state == GameState.PLAYER_1_WIN:
            text = "Player 1 Victory!"
            color = CYAN
        elif self.screen.engine.state == GameState.PLAYER_2_WIN:
            p2_label = "Player 2" if self.screen.mode == GameMode.PVP else "CPU"
            text = f"{p2_label} Victory!"
            color = RED
        else:
            text = "Draw Game!"
            color = DARK_TEAL
            
        panel_w, panel_h = 550, 250
        panel_rect = pygame.Rect(WIDTH//2 - panel_w//2, HEIGHT//2 - panel_h//2, panel_w, panel_h)
        
        # Outer Glow for Panel
        for i in range(15, 0, -3):
            pygame.draw.rect(self.screen.screen, (*color, 50//i), panel_rect.inflate(i*2, i*2), border_radius=30)
            
        pygame.draw.rect(self.screen.screen, WHITE, panel_rect, border_radius=30)
        pygame.draw.rect(self.screen.screen, color, panel_rect, 5, border_radius=30)
        
        # Winner Text with Shadow-like offset for depth
        draw_text(self.screen.screen, text, WIDTH // 2, HEIGHT // 2 - 30, self.screen.title_font, color)
        draw_text(self.screen.screen, "TAP ANYWHERE TO CONTINUE", WIDTH // 2, HEIGHT // 2 + 55, self.screen.small_font, DARK_TEAL)
