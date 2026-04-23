import pygame
import sys
import time
from constants import *
from logic.game_engine import GameEngine, GameState, GameMode
from ai.bot import AIBot
from ui.menu_ui import MenuRenderer
from ui.game_ui import GameRenderer
from ui.start_ui import StartRenderer
from ui.audio_manager import AudioManager
from ui.audio_settings_ui import AudioSettingsUI

class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Dots and Boxes")
        self.clock = pygame.time.Clock()
        
        # Load and Resize Icons
        self._load_icons()

        try:
            self.title_font = pygame.font.SysFont("segoeui", 72, bold=True)
            self.font = pygame.font.SysFont("segoeui", 24, bold=True)
            self.small_font = pygame.font.SysFont("segoeui", 20)
            self.play_font = pygame.font.SysFont("segoeui", 48, bold=True)
            self.label_font = pygame.font.SysFont("segoeui", 32, bold=True)
        except:
            self.title_font = pygame.font.Font(None, 72)
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 20)
            self.play_font = pygame.font.Font(None, 48)
            self.label_font = pygame.font.Font(None, 32)
            
        self.engine = None
        self.bot = None
        self.state = 'START_SCREEN'
        self.previous_state = 'START_SCREEN'
        
        self.mode = GameMode.PVE
        self.difficulty = 'medium'
        self.board_size = (3, 3)
        self.is_quickplay = False
        
        self.show_dropdown = False
        self.show_diff_dropdown = False
        #Custom Board
        self.choosing_custom_row = False
        self.choosing_custom_col = False

        self.show_help = False
        
        self.margin_x = 0
        self.margin_y = 0
        self.square_size = SQUARE_SIZE
        
        self.mouse_pos = (0, 0)
        self.last_move = None
        self.hovered_edge = None
        self.dot_radius = DOT_RADIUS
        
        # Audio
        self.audio_manager = AudioManager()
        self.audio_manager.play_bgm()

        #Gọi UI
        self.menu_renderer = MenuRenderer(self)
        self.game_renderer = GameRenderer(self)
        self.start_renderer = StartRenderer(self)
        self.audio_settings_ui = AudioSettingsUI(self, self.audio_manager)

    @property
    def sound_on(self):
        return not self.audio_manager.is_muted

    def _load_icons(self):
        icon_path = "ui/icon/"
        try:
            self.icons = {
                "arrow": pygame.transform.smoothscale(pygame.image.load(icon_path + "tamgiac.png").convert_alpha(), (30, 30)),
                "dropdown": pygame.transform.smoothscale(pygame.image.load(icon_path + "muitenxuong.png").convert_alpha(), (30, 25)),
                "close": pygame.transform.smoothscale(pygame.image.load(icon_path + "dauX.png").convert_alpha(), (30, 30)),
                "user": pygame.transform.smoothscale(pygame.image.load(icon_path + "nguoi.png").convert_alpha(), (50, 50)),
                "user2": pygame.transform.smoothscale(pygame.image.load(icon_path + "nguoi2.png").convert_alpha(), (50, 50)),
                "robot": pygame.transform.smoothscale(pygame.image.load(icon_path + "bot.png").convert_alpha(), (50, 50)),
                "home": pygame.transform.smoothscale(pygame.image.load(icon_path + "home.png").convert_alpha(), (40, 40)),
                "restart": pygame.transform.smoothscale(pygame.image.load(icon_path + "reload.png").convert_alpha(), (40, 40)),
            }
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.icons = {}

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
        
        available_width = WIDTH - 100
        available_height = HEIGHT - 260
        max_square_width = available_width // cols
        max_square_height = available_height // rows
        self.square_size = min(max_square_width, max_square_height, 120)
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
            
            if self.state == 'AUDIO_SETTINGS':
                self.audio_settings_ui.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                    # If we don't return here, it might trigger other clicks if coordinates overlap
                    # but since we are in AUDIO_SETTINGS state, other blocks won't execute anyway.
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Global Help Overlay Close
                if self.show_help:
                    # Match close_y = 620 (620 - 30 = 590)
                    help_close_rect = pygame.Rect(WIDTH//2 - 30, 590, 60, 60)
                    if help_close_rect.collidepoint(x, y):
                        self.show_help = False
                    return
                    
                # Start screen
                if self.state == 'START_SCREEN':
                    # Sound button
                    if (x - 60)**2 + (y - (HEIGHT - 60))**2 <= 30**2:
                        self.previous_state = self.state
                        self.state = 'AUDIO_SETTINGS'
                        return
                    # Start game button
                    if self.start_renderer.start_game_rect.collidepoint(x, y):
                        self._start_game()
                    elif self.start_renderer.settings_rect.collidepoint(x, y):
                        self.state = 'MAIN_MENU'
                    elif self.start_renderer.exit_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                elif self.state == 'MAIN_MENU':
                    self._handle_menu_click(x, y)
                elif self.state == 'IN_GAME' and self.engine.state == GameState.IN_GAME:
                    nav_y = HEIGHT - 60
                    nav_center_x = WIDTH // 2
                    # Sound button
                    if (x - 60)**2 + (y - nav_y)**2 <= 30**2:
                        self.previous_state = self.state
                        self.state = 'AUDIO_SETTINGS'
                        return
                    # Home button
                    elif (x - (nav_center_x - 55))**2 + (y - nav_y)**2 <= 42**2:
                        self.state = 'START_SCREEN'
                        return
                    # Restart button
                    elif (x - (nav_center_x + 55))**2 + (y - nav_y)**2 <= 42**2:
                        self._start_game()
                        return
                    # Help button
                    elif (x - (WIDTH - 60))**2 + (y - nav_y)**2 <= 30**2:
                        self.show_help = True
                        return
                    # Game area
                    if self.engine.current_player == 1 or self.engine.mode == GameMode.PVP:
                        move = self._get_move_from_mouse(x, y)
                        if move and move in self.engine.board.get_possible_moves():
                            score = self.engine.make_move(move)
                            self.last_move = move
                            if score is not None:
                                if score > 0:
                                    self.audio_manager.play_sfx('score')
                                else:
                                    self.audio_manager.play_sfx('move')
                # Game over screen
                elif self.state == 'GAME_OVER':
                    self.state = 'START_SCREEN'

    def _handle_menu_click(self, x, y):
        # Handle Board Dropdown options
        if self.show_dropdown:
            options = ["Small", "Medium", "Large", "Custom"] # Thêm Custom vào danh sách
            btn_start_x = 310
            start_y = 500 # Đồng bộ với MenuRenderer
            for i, opt in enumerate(options):
                # Thêm + 20 để khớp với tọa độ vẽ
                rect = pygame.Rect(btn_start_x + 20, start_y + i * 60, 190, 60)
                if rect.collidepoint(x, y):
                    if opt == "Small": self.board_size = (3, 3)
                    elif opt == "Medium": self.board_size = (5, 5)
                    elif opt == "Large": self.board_size = (7, 7)
                    elif opt == "Custom": self.board_size = (10, 10)
                    self.show_dropdown = False
                    return
            self.show_dropdown = False 
            return

        # Handle Custom Number Picker
        if self.choosing_custom_row or self.choosing_custom_col:
            picker_x = WIDTH // 2 - 150
            picker_y = HEIGHT // 2 - 150
            for i in range(19): # Numbers 2 to 20
                num = i + 2
                row, col = i // 5, i % 5
                btn_size = 60
                btn_rect = pygame.Rect(picker_x + col * btn_size, picker_y + row * btn_size, btn_size, btn_size)
                if btn_rect.collidepoint(x, y):
                    r, c = self.board_size
                    if self.choosing_custom_row: self.board_size = (num, c)
                    else: self.board_size = (r, num)
                    self.choosing_custom_row = False
                    self.choosing_custom_col = False
                    return
            self.choosing_custom_row = False
            self.choosing_custom_col = False
            return

        # Handle Difficulty Dropdown options
        if self.show_diff_dropdown:
            options = ["Easy", "Medium", "Hard"]
            btn_start_x = 310
            start_y = 430
            for i, opt in enumerate(options):
                rect = pygame.Rect(btn_start_x, start_y + i * 60, 190, 60)
                if rect.collidepoint(x, y):
                    self.difficulty = opt.lower()
                    self.show_diff_dropdown = False
                    return
            self.show_diff_dropdown = False 
            return

        # Handle Bottom UI
        if (x - 60)**2 + (y - (HEIGHT - 60))**2 <= 30**2:
            self.previous_state = self.state
            self.state = 'AUDIO_SETTINGS'
            return
        play_rect = pygame.Rect(WIDTH//2 - 120, 660, 240, 100)
        if play_rect.collidepoint(x, y):
            self.state = 'START_SCREEN'
            return
        help_rect = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
        if help_rect.collidepoint(x, y):
            self.show_help = True
            return

        # Handle Settings Rows
        btn_start_x = 310
        row_y = 305
        spacing = 80

        # Players
        if row_y - 30 <= y <= row_y + 30:
            if btn_start_x <= x <= btn_start_x + 90: self.mode = GameMode.PVE
            elif btn_start_x + 100 <= x <= btn_start_x + 190: self.mode = GameMode.PVP
        
        # Difficulty Dropdown
        row_y += spacing
        if self.mode == GameMode.PVE:
            diff_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 190, 60)
            if diff_rect.collidepoint(x, y):
                self.show_diff_dropdown = not self.show_diff_dropdown
                self.show_dropdown = False # Close other dropdown
                return

        # Board Dropdown
        row_y += spacing
        board_rect = pygame.Rect(btn_start_x + 20, row_y - 30, 190, 60)
        if board_rect.collidepoint(x, y):
            self.show_dropdown = not self.show_dropdown
            self.show_diff_dropdown = False # Close other dropdown
            return

        # Custom Size Inputs Click Detection
        if self.board_size_name == "Custom":
            r_rect = pygame.Rect(btn_start_x + 220, row_y - 30, 60, 60)
            c_rect = pygame.Rect(btn_start_x + 300, row_y - 30, 60, 60)
            if r_rect.collidepoint(x, y):
                self.choosing_custom_row = True
                self.choosing_custom_col = False
                return
            if c_rect.collidepoint(x, y):
                self.choosing_custom_col = True
                self.choosing_custom_row = False
                return

        # Quick Game
        row_y += spacing
        if row_y - 30 <= y <= row_y + 30:
            if btn_start_x <= x <= btn_start_x + 90: self.is_quickplay = True
            elif btn_start_x + 100 <= x <= btn_start_x + 190: self.is_quickplay = False

        # Audio Settings Button
        if WIDTH//2 - 120 <= x <= WIDTH//2 + 120 and 620 <= y <= 680:
            self.state = 'AUDIO_SETTINGS'

    def _update(self):
        if self.state == 'IN_GAME':
            self.engine.update()
            if self.engine.state in [GameState.PLAYER_1_WIN, GameState.PLAYER_2_WIN, GameState.DRAW]:
                self.state = 'GAME_OVER'
                # Play outcome sound: Player 1 is always the human
                if self.engine.state == GameState.PLAYER_1_WIN:
                    self.audio_manager.play_sfx('winner')
                else:
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

    def _draw(self):
        self.screen.fill(BG_COLOR)
        if self.state == 'START_SCREEN':
            self.start_renderer.draw()
        elif self.state == 'MAIN_MENU':
            self.menu_renderer.draw()
        elif self.state == 'IN_GAME':
            self.game_renderer.draw_board()
            if self.show_help:
                self.menu_renderer.draw_help_overlay()
        elif self.state == 'GAME_OVER':
            self.game_renderer.draw_board()
            self.game_renderer.draw_game_over()
        elif self.state == 'AUDIO_SETTINGS':
            self.audio_settings_ui.draw()
        pygame.display.flip()
