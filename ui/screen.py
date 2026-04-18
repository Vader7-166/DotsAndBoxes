import pygame
import sys
import time
from constants import *
from logic.game_engine import GameEngine, GameState, GameMode
from ai.bot import AIBot
from ui.audio_manager import AudioManager
from ui.audio_settings_ui import AudioSettingsUI

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Dots and Boxes")
        self.clock = pygame.time.Clock()
        
        self.audio_manager = AudioManager()
        self.audio_manager.play_bgm()
        self.audio_settings_ui = AudioSettingsUI(self, self.audio_manager)
        
        try:
            self.title_font = pygame.font.SysFont("segoeui", 60, bold=True)
            self.font = pygame.font.SysFont("segoeui", 36)
            self.small_font = pygame.font.SysFont("segoeui", 24)
        except:
            self.title_font = pygame.font.Font(None, 60)
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            
        self.engine = None
        self.bot = None
        self.state = 'MAIN_MENU'
        
        self.mode = GameMode.PVE
        self.difficulty = 'medium'
        self.board_size = (3, 3)
        self.is_quickplay = False
        
        self.margin_x = 0
        self.margin_y = 0
        self.square_size = SQUARE_SIZE
        
        self.mouse_pos = (0, 0)
        self.last_move = None
        self.hovered_edge = None
        self.show_help = False

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)

    def _start_game(self):
        rows, cols = self.board_size
        self.engine = GameEngine(rows, cols, self.mode, self.is_quickplay)
        self.last_move = None
        
        if self.mode == GameMode.PVE:
            self.bot = AIBot(difficulty=self.difficulty, player_id=2)
            
        self.engine.start_game()
        self.state = 'IN_GAME'
        
        # Tự động tính toán kích thước ô (square_size) dựa trên kích thước bảng
        # Dành ra 160px cho UI phía trên và 100px cho UI phía dưới
        available_width = WIDTH - 100 # padding 50px mỗi bên
        available_height = HEIGHT - 260 # padding top 160, bottom 100
        
        max_square_width = available_width // cols
        max_square_height = available_height // rows
        
        self.square_size = min(max_square_width, max_square_height, 120) # Giới hạn max là 120px
        
        # Căn giữa bảng
        self.margin_x = (WIDTH - (cols * self.square_size)) // 2
        self.margin_y = 120 + (available_height - (rows * self.square_size)) // 2

    def _handle_events(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.hovered_edge = None
        
        if self.state == 'IN_GAME' and self.engine.state == GameState.IN_GAME and not self.show_help:
            self.hovered_edge = self._get_move_from_mouse(self.mouse_pos[0], self.mouse_pos[1])
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if self.show_help:
                    self.show_help = False
                    continue

                # Handle Navigation Buttons (Quit/Help)
                if self.state not in ['SETTINGS', 'AUDIO_SETTINGS']:
                    # Quit Button
                    if NAV_MARGIN <= x <= NAV_MARGIN + NAV_BUTTON_WIDTH and \
                       HEIGHT - NAV_BUTTON_HEIGHT - NAV_MARGIN <= y <= HEIGHT - NAV_MARGIN:
                        if self.state == 'IN_GAME' or self.state == 'GAME_OVER':
                            self.state = 'MAIN_MENU'
                        else:
                            pygame.quit()
                            sys.exit()
                    
                    # Help Button
                    if WIDTH - NAV_BUTTON_WIDTH - NAV_MARGIN <= x <= WIDTH - NAV_MARGIN and \
                       HEIGHT - NAV_BUTTON_HEIGHT - NAV_MARGIN <= y <= HEIGHT - NAV_MARGIN:
                        self.show_help = True
                        continue

                if self.state == 'MAIN_MENU':
                    self._handle_menu_click(x, y)
                elif self.state == 'SETTINGS':
                    self._handle_settings_click(x, y)
                elif self.state == 'AUDIO_SETTINGS':
                    self.audio_settings_ui.handle_click(x, y)
                elif self.state == 'IN_GAME' and self.engine.state == GameState.IN_GAME:
                    if self.engine.current_player == 1 or self.engine.mode == GameMode.PVP:
                        move = self._get_move_from_mouse(x, y)
                        if move and move in self.engine.board.get_possible_moves():
                            score = self.engine.make_move(move)
                            if score is not None:
                                self.last_move = move
                                if score > 0:
                                    self.audio_manager.play_sfx('score')
                                else:
                                    self.audio_manager.play_sfx('move')
                elif self.state == 'GAME_OVER':
                    self.state = 'MAIN_MENU'

    def _handle_menu_click(self, x, y):
        if WIDTH//2 - 120 <= x <= WIDTH//2 + 120 and HEIGHT//2 - 50 <= y <= HEIGHT//2 + 20:
            self._start_game()
        elif WIDTH//2 - 120 <= x <= WIDTH//2 + 120 and HEIGHT//2 + 40 <= y <= HEIGHT//2 + 110:
            self.state = 'SETTINGS'

    def _handle_settings_click(self, x, y):
        if 20 <= x <= 220 and HEIGHT - 80 <= y <= HEIGHT - 30:
            self.state = 'MAIN_MENU'
            
        # Điều chỉnh vùng click cho Settings (màn hình rộng hơn)
        if 220 <= y <= 270:
            if 300 <= x <= 400: self.board_size = (3, 3)
            elif 420 <= x <= 520: self.board_size = (5, 5)
            elif 540 <= x <= 640: self.board_size = (7, 7)
            
        if 320 <= y <= 370:
            if 300 <= x <= 450: self.mode = GameMode.PVP
            elif 470 <= x <= 620: self.mode = GameMode.PVE
            
        if self.mode == GameMode.PVE and 420 <= y <= 470:
            if 300 <= x <= 400: self.difficulty = 'easy'
            elif 420 <= x <= 520: self.difficulty = 'medium'
            elif 540 <= x <= 640: self.difficulty = 'hard'
            
        if 520 <= y <= 570:
            if 300 <= x <= 450: self.is_quickplay = True
            elif 470 <= x <= 620: self.is_quickplay = False

        # Audio Settings Button
        if WIDTH//2 - 120 <= x <= WIDTH//2 + 120 and 620 <= y <= 680:
            self.state = 'AUDIO_SETTINGS'

    def _update(self):
        if self.state == 'IN_GAME':
            self.engine.update()
            
            if self.engine.state in [GameState.PLAYER_1_WIN, GameState.PLAYER_2_WIN, GameState.DRAW]:
                self.state = 'GAME_OVER'
                self.audio_manager.play_sfx('gameover')
                return

            if self.engine.mode == GameMode.PVE and self.engine.current_player == 2 and self.engine.state == GameState.IN_GAME:
                pygame.time.delay(600)
                move = self.bot.get_move(self.engine.board)
                if move:
                    score = self.engine.make_move(move)
                    if score is not None:
                        self.last_move = move
                        if score > 0:
                            self.audio_manager.play_sfx('score')
                        else:
                            self.audio_manager.play_sfx('move')

    def _get_move_from_mouse(self, x, y):
        rows, cols = self.board_size
        hitbox = 20
        
        for r in range(rows + 1):
            for c in range(cols):
                if not self.engine.board.h_edges[r][c]:
                    edge_rect = pygame.Rect(
                        self.margin_x + c * self.square_size + DOT_RADIUS,
                        self.margin_y + r * self.square_size - hitbox,
                        self.square_size - 2 * DOT_RADIUS,
                        hitbox * 2
                    )
                    if edge_rect.collidepoint(x, y):
                        return ('h', r, c)
                    
        for r in range(rows):
            for c in range(cols + 1):
                if not self.engine.board.v_edges[r][c]:
                    edge_rect = pygame.Rect(
                        self.margin_x + c * self.square_size - hitbox,
                        self.margin_y + r * self.square_size + DOT_RADIUS,
                        hitbox * 2,
                        self.square_size - 2 * DOT_RADIUS
                    )
                    if edge_rect.collidepoint(x, y):
                        return ('v', r, c)
                    
        return None

    def _draw_text(self, text, x, y, font, color=BLACK, align="center"):
        img = font.render(text, True, color)
        if align == "center":
            rect = img.get_rect(center=(x, y))
        elif align == "left":
            rect = img.get_rect(midleft=(x, y))
        else:
            rect = img.get_rect(midright=(x, y))
        self.screen.blit(img, rect)

    def _draw_button(self, text, x, y, w, h, is_active=False):
        color = BLACK if is_active else WHITE
        text_color = WHITE if is_active else BLACK
        
        rect = pygame.Rect(x, y, w, h)
        
        if rect.collidepoint(self.mouse_pos) and not is_active:
            color = HOVER_COLOR
            
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=10)
        self._draw_text(text, x + w//2, y + h//2, self.font, text_color)

    def _draw(self):
        self.screen.fill(BG_COLOR)
        
        if self.state == 'MAIN_MENU':
            self._draw_text("DOTS AND BOXES", WIDTH//2, HEIGHT//2 - 150, self.title_font, BLACK)
            self._draw_button("START GAME", WIDTH//2 - 120, HEIGHT//2 - 50, 240, 70)
            self._draw_button("SETTINGS", WIDTH//2 - 120, HEIGHT//2 + 40, 240, 70)
            
        elif self.state == 'SETTINGS':
            self._draw_text("GAME SETTINGS", WIDTH//2, 80, self.title_font, BLACK)
            
            # Căn lề trái cho nhãn Setting
            label_x = 100
            
            self._draw_text("Board Size", label_x, 245, self.font, align="left")
            self._draw_button("3x3", 300, 220, 100, 50, self.board_size == (3, 3))
            self._draw_button("5x5", 420, 220, 100, 50, self.board_size == (5, 5))
            self._draw_button("7x7", 540, 220, 100, 50, self.board_size == (7, 7))
            
            self._draw_text("Game Mode", label_x, 345, self.font, align="left")
            self._draw_button("PvP", 300, 320, 150, 50, self.mode == GameMode.PVP)
            self._draw_button("PvE", 470, 320, 150, 50, self.mode == GameMode.PVE)
            
            if self.mode == GameMode.PVE:
                self._draw_text("Bot Difficulty", label_x, 445, self.font, align="left")
                self._draw_button("Easy", 300, 420, 100, 50, self.difficulty == 'easy')
                self._draw_button("Medium", 420, 420, 100, 50, self.difficulty == 'medium')
                self._draw_button("Hard", 540, 420, 100, 50, self.difficulty == 'hard')
                
            self._draw_text("Quickplay", label_x, 545, self.font, align="left")
            self._draw_button("Enabled", 300, 520, 150, 50, self.is_quickplay)
            self._draw_button("Disabled", 470, 520, 150, 50, not self.is_quickplay)

            self._draw_button("AUDIO SETTINGS", WIDTH//2 - 120, 620, 240, 60)
            self._draw_button("Back to Menu", 20, HEIGHT - 80, 200, 50)
            
        elif self.state == 'AUDIO_SETTINGS':
            self.audio_settings_ui.draw()
            
        elif self.state == 'IN_GAME':
            self._draw_board()
        elif self.state == 'GAME_OVER':
            self._draw_board()
            self._draw_game_over()
            
        self._draw_navigation()
        
        if self.show_help:
            self._draw_help_overlay()
            
        pygame.display.flip()

    def _draw_board(self):
        board = self.engine.board
        rows, cols = self.board_size
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 0, WIDTH, 80))
        pygame.draw.line(self.screen, GRAY, (0, 80), (WIDTH, 80), 2)
        
        p1_text = f"Player 1: {board.get_score(1)}"
        p2_label = "Player 2" if self.mode == GameMode.PVP else "Bot"
        p2_text = f"{p2_label}: {board.get_score(2)}"
        
        self._draw_text(p1_text, 150, 40, self.font, P1_COLOR)
        self._draw_text(p2_text, WIDTH - 150, 40, self.font, P2_COLOR)

        if self.engine.is_quickplay and self.engine.turn_start_time:
            time_left = max(0, int(self.engine.turn_time_limit - (time.time() - self.engine.turn_start_time)))
            color = RED if time_left <= 3 else BLACK
            self._draw_text(f"00:{time_left:02d}", WIDTH // 2, 40, self.title_font, color)

        for r in range(rows):
            for c in range(cols):
                owner = board.boxes[r][c]
                if owner != 0:
                    color = P1_LIGHT_COLOR if owner == 1 else P2_LIGHT_COLOR
                    rect = pygame.Rect(
                        self.margin_x + c * self.square_size,
                        self.margin_y + r * self.square_size,
                        self.square_size,
                        self.square_size
                    )
                    pygame.draw.rect(self.screen, color, rect)

        if self.hovered_edge and self.engine.current_player == 1:
            d, r, c = self.hovered_edge
            hover_color = P1_LIGHT_COLOR
            if d == 'h':
                pygame.draw.line(self.screen, hover_color,
                    (self.margin_x + c * self.square_size + DOT_RADIUS, self.margin_y + r * self.square_size),
                    (self.margin_x + (c + 1) * self.square_size - DOT_RADIUS, self.margin_y + r * self.square_size),
                    HOVER_EDGE_WIDTH)
            else:
                pygame.draw.line(self.screen, hover_color,
                    (self.margin_x + c * self.square_size, self.margin_y + r * self.square_size + DOT_RADIUS),
                    (self.margin_x + c * self.square_size, self.margin_y + (r + 1) * self.square_size - DOT_RADIUS),
                    HOVER_EDGE_WIDTH)

        for r in range(rows + 1):
            for c in range(cols):
                if board.h_edges[r][c]:
                    owner = board.h_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    width = EDGE_WIDTH
                    
                    if self.last_move == ('h', r, c):
                        width = EDGE_WIDTH + 4
                        color = BLACK
                        
                    pygame.draw.line(
                        self.screen, color,
                        (self.margin_x + c * self.square_size, self.margin_y + r * self.square_size),
                        (self.margin_x + (c + 1) * self.square_size, self.margin_y + r * self.square_size),
                        width
                    )

        for r in range(rows):
            for c in range(cols + 1):
                if board.v_edges[r][c]:
                    owner = board.v_edge_owners[r][c]
                    color = P1_COLOR if owner == 1 else P2_COLOR
                    width = EDGE_WIDTH
                    
                    if self.last_move == ('v', r, c):
                        width = EDGE_WIDTH + 4
                        color = BLACK
                        
                    pygame.draw.line(
                        self.screen, color,
                        (self.margin_x + c * self.square_size, self.margin_y + r * self.square_size),
                        (self.margin_x + c * self.square_size, self.margin_y + (r + 1) * self.square_size),
                        width
                    )

        for r in range(rows + 1):
            for c in range(cols + 1):
                pygame.draw.circle(
                    self.screen, BLACK,
                    (self.margin_x + c * self.square_size, self.margin_y + r * self.square_size),
                    DOT_RADIUS
                )
                pygame.draw.circle(
                    self.screen, WHITE,
                    (self.margin_x + c * self.square_size, self.margin_y + r * self.square_size),
                    DOT_RADIUS // 2
                )

        turn_text = "Player 1's Turn" if self.engine.current_player == 1 else f"{p2_label}'s Turn"
        turn_color = P1_COLOR if self.engine.current_player == 1 else P2_COLOR
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, HEIGHT - 60, WIDTH, 60))
        pygame.draw.line(self.screen, GRAY, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 2)
        self._draw_text(turn_text, WIDTH // 2, HEIGHT - 30, self.font, turn_color)

    def _draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        if self.engine.state == GameState.PLAYER_1_WIN:
            text = "Player 1 Wins!"
            color = P1_COLOR
        elif self.engine.state == GameState.PLAYER_2_WIN:
            p2_label = "Player 2" if self.mode == GameMode.PVP else "Bot"
            text = f"{p2_label} Wins!"
            color = P2_COLOR
        else:
            text = "It's a Draw!"
            color = BLACK
            
        panel_rect = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 100, 500, 200)
        pygame.draw.rect(self.screen, WHITE, panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, color, panel_rect, 4, border_radius=15)
        
        self._draw_text(text, WIDTH // 2, HEIGHT // 2 - 20, self.title_font, color)
        self._draw_text("Click anywhere to return to Menu", WIDTH // 2, HEIGHT // 2 + 50, self.small_font, GRAY)

    def _draw_navigation(self):
        if self.state in ['SETTINGS', 'AUDIO_SETTINGS']:
            return
            
        # Quit Button (Bottom Left)
        self._draw_button("QUIT", NAV_MARGIN, HEIGHT - NAV_BUTTON_HEIGHT - NAV_MARGIN, 
                          NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)
        
        # Help Button (Bottom Right)
        self._draw_button("HELP", WIDTH - NAV_BUTTON_WIDTH - NAV_MARGIN, 
                          HEIGHT - NAV_BUTTON_HEIGHT - NAV_MARGIN, 
                          NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT)

    def _draw_help_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        self._draw_text("HOW TO PLAY", WIDTH // 2, 150, self.title_font, BLACK)
        
        rules = [
            "1. Players take turns clicking on grid edges to draw a line.",
            "2. If you complete a 1x1 box, you score a point and get another turn.",
            "3. The game ends when all edges are drawn.",
            "4. The player with the most points wins!",
            "",
            "Controls:",
            "- Click edges to place lines",
            "- Use SETTINGS to change board size or mode",
            "- Press anywhere to close this help screen"
        ]
        
        for i, line in enumerate(rules):
            self._draw_text(line, WIDTH // 2, 250 + i * 40, self.font, BLACK)
            
        self._draw_text("Click to Close", WIDTH // 2, HEIGHT - 100, self.small_font, GRAY)
