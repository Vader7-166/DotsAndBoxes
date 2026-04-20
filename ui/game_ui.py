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
        
        pygame.draw.circle(self.screen.screen, (175, 238, 238), (120, 60), 25)
        draw_text(self.screen.screen, str(board.get_score(1)), 120, 60, self.screen.font, DARK_TEAL)
        
        p2_center = (WIDTH - 60, 60)
        pygame.draw.circle(self.screen.screen, RED, p2_center, 40)
        if self.screen.engine.current_player == 2:
            # Active indicator: Thick RED ring
            pygame.draw.circle(self.screen.screen, RED, p2_center, 48, 5)
            
        p2_icon_key = "user" if self.screen.mode == GameMode.PVP else "robot"
        if p2_icon_key in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons[p2_icon_key], p2_center[0], p2_center[1], center=True)
        else:
            p2_label_icon = "P2" if self.screen.mode == GameMode.PVP else "AI"
            draw_text(self.screen.screen, p2_label_icon, p2_center[0], p2_center[1], self.screen.font, WHITE)
        
        pygame.draw.circle(self.screen.screen, (255, 193, 193), (WIDTH - 120, 60), 25)
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
                    (self.screen.margin_x + c * self.screen.square_size + DOT_RADIUS, self.screen.margin_y + r * self.screen.square_size),
                    (self.screen.margin_x + (c + 1) * self.screen.square_size - DOT_RADIUS, self.screen.margin_y + r * self.screen.square_size),
                    HOVER_EDGE_WIDTH)
            else:
                pygame.draw.line(self.screen.screen, hover_color,
                    (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + r * self.screen.square_size + DOT_RADIUS),
                    (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + (r + 1) * self.screen.square_size - DOT_RADIUS),
                    HOVER_EDGE_WIDTH)

        # Edges
        for r in range(rows + 1):
            for c in range(cols):
                if board.h_edges[r][c]:
                    owner = board.h_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    pygame.draw.line(
                        self.screen.screen, color,
                        (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + r * self.screen.square_size),
                        (self.screen.margin_x + (c + 1) * self.screen.square_size, self.screen.margin_y + r * self.screen.square_size),
                        EDGE_WIDTH
                    )

        for r in range(rows):
            for c in range(cols + 1):
                if board.v_edges[r][c]:
                    owner = board.v_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    pygame.draw.line(
                        self.screen.screen, color,
                        (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + r * self.screen.square_size),
                        (self.screen.margin_x + c * self.screen.square_size, self.screen.margin_y + (r + 1) * self.screen.square_size),
                        EDGE_WIDTH
                    )

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
        
        # Home button
        pygame.draw.circle(self.screen.screen, CYAN, (nav_center_x - 55, nav_y), 42)
        if "home" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["home"], nav_center_x - 55, nav_y, center=True)
        else:
            draw_text(self.screen.screen, "H", nav_center_x - 55, nav_y, self.screen.font, WHITE)
        
        # Restart button
        pygame.draw.circle(self.screen.screen, CYAN, (nav_center_x + 55, nav_y), 42)
        if "restart" in self.screen.icons:
            draw_icon(self.screen.screen, self.screen.icons["restart"], nav_center_x + 55, nav_y, center=True)
        else:
            draw_text(self.screen.screen, "R", nav_center_x + 55, nav_y, self.screen.font, WHITE)
        
        # Help button
        pygame.draw.circle(self.screen.screen, CYAN, (WIDTH - 60, nav_y), 30)
        draw_text(self.screen.screen, "?", WIDTH - 60, nav_y, self.screen.font, WHITE)

        # Speaker button (Bottom Left)
        draw_speaker(self.screen.screen, 60, HEIGHT - 60, self.screen.sound_on)

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
