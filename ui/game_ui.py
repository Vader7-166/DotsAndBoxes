from constants import P2_LIGHT_COLOR
import pygame
import time
from constants import *
from ui.utils import draw_text, draw_speaker, draw_icon
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

        # Hovered Edge
        if self.screen.hovered_edge and self.screen.engine.current_player == 1:
            d, r, c = self.screen.hovered_edge
            hover_color = P1_LIGHT_COLOR
            if d == 'h':
                pygame.draw.line(self.screen.screen, hover_color,
                    (self.screen.margin_x + c * self.screen.square_size + self.screen.dot_radius, self.screen.margin_y + r * self.screen.square_size),
                    (self.screen.margin_x + (c + 1) * self.screen.square_size - self.screen.dot_radius, self.screen.margin_y + r * self.screen.square_size),
                    HOVER_EDGE_WIDTH)
            else:
                pygame.draw.line(self.screen.screen, hover_color,
                    (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + r * self.screen.square_size + self.screen.dot_radius),
                    (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + (r + 1) * self.screen.square_size - self.screen.dot_radius),
                    HOVER_EDGE_WIDTH)

        # Edges
        for r in range(rows + 1):
            for c in range(cols):
                if board.h_edges[r][c]:
                    owner = board.h_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    # Highlight last move
                    is_last = self.screen.last_move == ('h', r, c)
                    
                    s = self.screen.square_size
                    x1 = self.screen.margin_x + c * s
                    x2 = x1 + s
                    y = self.screen.margin_y + r * s
                    
                    # Bone shape parameters
                    flare = 20 if is_last else 18
                    mid = 17 if is_last else 15
                    gap = self.screen.dot_radius - 2
                    
                    points = [
                        (x1 + gap, y - flare//2), (x1 + s//2, y - mid//2), (x2 - gap, y - flare//2),
                        (x2 - gap, y + flare//2), (x1 + s//2, y + mid//2), (x1 + gap, y + flare//2)
                    ]
                    pygame.draw.polygon(self.screen.screen, color, points)

        for r in range(rows):
            for c in range(cols + 1):
                if board.v_edges[r][c]:
                    owner = board.v_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    # Highlight last move
                    is_last = self.screen.last_move == ('v', r, c)
                    
                    s = self.screen.square_size
                    x = self.screen.margin_x + c * s
                    y1 = self.screen.margin_y + r * s
                    y2 = y1 + s
                    
                    # Bone shape parameters
                    flare = 20 if is_last else 16
                    mid = 16 if is_last else 13
                    gap = DOT_RADIUS - 1
                    
                    points = [
                        (x - flare//2, y1 + gap), (x - mid//2, y1 + s//2), (x - flare//2, y2 - gap),
                        (x + flare//2, y2 - gap), (x + mid//2, y1 + s//2), (x + flare//2, y1 + gap)
                    ]
                    pygame.draw.polygon(self.screen.screen, color, points)

        # Dots
        for r in range(rows + 1):
            for c in range(cols + 1):
                dx = self.screen.margin_x + c * self.screen.square_size
                dy = self.screen.margin_y + r * self.screen.square_size
                pygame.draw.circle(self.screen.screen, (180, 200, 200), (dx, dy + 2), DOT_RADIUS)
                pygame.draw.circle(self.screen.screen, WHITE, (dx, dy), DOT_RADIUS)
                pygame.draw.circle(self.screen.screen, WHITE, (dx, dy), DOT_RADIUS // 2)

        # Navigation Bar
        nav_center_x = WIDTH // 2
        nav_y = HEIGHT - 60
        mouse_pos = pygame.mouse.get_pos()
        
        # Home button
        home_pos = (nav_center_x - 55, nav_y)
        home_rect = pygame.Rect(home_pos[0] - 42, home_pos[1] - 42, 84, 84)
        is_home_hovered = home_rect.collidepoint(mouse_pos)
        h_radius = 45 if is_home_hovered else 42
        # h_color = tuple(min(255, c + 30) for c in CYAN) if is_home_hovered else CYAN
        
        pygame.draw.circle(self.screen.screen, CYAN, home_pos, h_radius)
        draw_icon(self.screen.screen, self.screen.icons["home"], home_pos[0], home_pos[1], center=True)
        
        # Restart button
        restart_pos = (nav_center_x + 55, nav_y)
        restart_rect = pygame.Rect(restart_pos[0] - 42, restart_pos[1] - 42, 84, 84)
        is_restart_hovered = restart_rect.collidepoint(mouse_pos)
        r_radius = 45 if is_restart_hovered else 42
        # r_color = tuple(min(255, c + 30) for c in CYAN) if is_restart_hovered else CYAN
        
        pygame.draw.circle(self.screen.screen, CYAN, restart_pos, r_radius)
        draw_icon(self.screen.screen, self.screen.icons["restart"], restart_pos[0], restart_pos[1], center=True)
        
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
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(WHITE)
        self.screen.screen.blit(overlay, (0, 0))
        
        if self.screen.engine.state == GameState.PLAYER_1_WIN:
            text = "Player 1 Wins!"
            color = P1_COLOR
        elif self.screen.engine.state == GameState.PLAYER_2_WIN:
            p2_label = "Player 2" if self.screen.mode == GameMode.PVP else "Bot"
            text = f"{p2_label} Wins!"
            color = P2_COLOR
        else:
            text = "It's a Draw!"
            color = DARK_TEAL
            
        panel_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 100, 500, 200)
        pygame.draw.rect(self.screen.screen, WHITE, panel_rect, border_radius=25)
        pygame.draw.rect(self.screen.screen, color, panel_rect, 4, border_radius=25)
        
        draw_text(self.screen.screen, text, WIDTH // 2, HEIGHT // 2 - 20, self.screen.title_font, color)
        draw_text(self.screen.screen, "Click anywhere to return to Menu", WIDTH // 2, HEIGHT // 2 + 50, self.screen.small_font, DARK_TEAL)
