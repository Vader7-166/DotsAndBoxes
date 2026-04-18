import pygame
import sys
import time
from constants import *
from logic.game_engine import GameEngine, GameState, GameMode
from ai.bot import AIBot
from ui.menu_ui import MenuRenderer

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Dots and Boxes")
        self.clock = pygame.time.Clock()
        
        try:
            self.title_font = pygame.font.SysFont("segoeui", 72, bold=True)
            self.font = pygame.font.SysFont("segoeui", 28, bold=True)
            self.small_font = pygame.font.SysFont("segoeui", 20)
            self.play_font = pygame.font.SysFont("segoeui", 48, bold=True)
            self.label_font = pygame.font.SysFont("segoeui", 32, bold=True)
        except:
            self.title_font = pygame.font.Font(None, 72)
            self.play_font = pygame.font.Font(None, 48)
            self.label_font = pygame.font.Font(None, 32)
            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 20)
            
        self.engine = None
        self.bot = None
        self.state = 'MAIN_MENU'
        
        self.mode = GameMode.PVE
        self.difficulty = 'medium'
        self.board_size = (3, 3)
        self.is_quickplay = False
        
        self.show_dropdown = False
        self.show_help = False
        
        self.margin_x = 0
        self.margin_y = 0
        self.square_size = SQUARE_SIZE
        
        self.mouse_pos = (0, 0)
        self.last_move = None
        self.hovered_edge = None

        #Gọi UI
        self.menu_renderer = MenuRenderer(self)

    @property
    def board_size_name(self):
        mapping = {(3, 3): "Small", (5, 5): "Medium", (7, 7): "Large"}
        return mapping.get(self.board_size, "Custom")

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
        
        if self.state == 'IN_GAME' and self.engine.state == GameState.IN_GAME:
            self.hovered_edge = self._get_move_from_mouse(self.mouse_pos[0], self.mouse_pos[1])
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if self.state == 'MAIN_MENU':
                    self._handle_menu_click(x, y)
                elif self.state == 'SETTINGS':
                    self._handle_settings_click(x, y)
                elif self.state == 'IN_GAME' and self.engine.state == GameState.IN_GAME:
                    if self.engine.current_player == 1 or self.engine.mode == GameMode.PVP:
                        move = self._get_move_from_mouse(x, y)
                        if move and move in self.engine.board.get_possible_moves():
                            self.engine.make_move(move)
                            self.last_move = move
                elif self.state == 'GAME_OVER':
                    self.state = 'MAIN_MENU'

    def _handle_menu_click(self, x, y):
        if self.show_help:
            # Click to close help
            help_close_rect = pygame.Rect(WIDTH//2 - 30, 550, 60, 60)
            if help_close_rect.collidepoint(x, y):
                self.show_help = False
            return

        if self.show_dropdown:
            options = ["Small", "Medium", "Large", "Custom"]
            btn_start_x = 310
            start_y = 510
            for i, opt in enumerate(options):
                rect = pygame.Rect(btn_start_x, start_y + i * 60, 190, 60)
                if rect.collidepoint(x, y):
                    if opt == "Small": self.board_size = (3, 3)
                    elif opt == "Medium": self.board_size = (5, 5)
                    elif opt == "Large": self.board_size = (7, 7)
                    self.show_dropdown = False
                    return
            self.show_dropdown = False # Close if click outside
            return

        # Play Button
        play_rect = pygame.Rect(WIDTH//2 - 120, 660, 240, 100)
        if play_rect.collidepoint(x, y):
            self._start_game()
            return

        # Help Button
        help_rect = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
        if help_rect.collidepoint(x, y):
            self.show_help = True
            return

        # Settings click areas
        btn_start_x = 310
        row_y = 305
        spacing = 80

        # Players
        if row_y - 30 <= y <= row_y + 30:
            if btn_start_x <= x <= btn_start_x + 90: self.mode = GameMode.PVE
            elif btn_start_x + 100 <= x <= btn_start_x + 190: self.mode = GameMode.PVP
        
        # Difficulty
        row_y += spacing
        if self.mode == GameMode.PVE and row_y - 30 <= y <= row_y + 30:
            if btn_start_x <= x <= btn_start_x + 90: self.difficulty = 'medium'
            elif btn_start_x + 100 <= x <= btn_start_x + 190: self.difficulty = 'hard'

        # Board Dropdown
        row_y += spacing
        board_rect = pygame.Rect(btn_start_x, row_y - 30, 190, 60)
        if board_rect.collidepoint(x, y):
            self.show_dropdown = not self.show_dropdown

        # Quick Game
        row_y += spacing
        if row_y - 30 <= y <= row_y + 30:
            if btn_start_x <= x <= btn_start_x + 90: self.is_quickplay = True
            elif btn_start_x + 100 <= x <= btn_start_x + 190: self.is_quickplay = False

    def _handle_settings_click(self, x, y):
        # Removed as settings are now in Main Menu
        pass

    def _update(self):
        if self.state == 'IN_GAME':
            self.engine.update()
            
            if self.engine.state in [GameState.PLAYER_1_WIN, GameState.PLAYER_2_WIN, GameState.DRAW]:
                self.state = 'GAME_OVER'
                return

            if self.engine.mode == GameMode.PVE and self.engine.current_player == 2 and self.engine.state == GameState.IN_GAME:
                pygame.time.delay(600)
                move = self.bot.get_move(self.engine.board)
                if move:
                    self.engine.make_move(move)
                    self.last_move = move

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
            self.menu_renderer.draw()
            
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
            
            self._draw_button("Back to Menu", 20, HEIGHT - 80, 200, 50)
            
        elif self.state == 'IN_GAME':
            self._draw_board()
        elif self.state == 'GAME_OVER':
            self._draw_board()
            self._draw_game_over()
            
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
