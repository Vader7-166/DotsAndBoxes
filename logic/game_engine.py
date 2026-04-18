from enum import Enum
from logic.board import Board
import time
import random

class GameState(Enum):
    MENU = 1
    IN_GAME = 2
    PAUSED = 3
    PLAYER_1_WIN = 4
    PLAYER_2_WIN = 5
    DRAW = 6

class GameMode(Enum):
    PVP = 1
    PVE = 2

class GameEngine:
    def __init__(self, rows, cols, mode=GameMode.PVE, is_quickplay=False):
        self.rows = rows
        self.cols = cols
        self.board = Board(rows, cols)
        self.current_player = 1
        self.state = GameState.MENU
        self.mode = mode
        self.is_quickplay = is_quickplay
        self.turn_start_time = None
        self.turn_time_limit = 10 if is_quickplay else None
        
    def start_game(self):
        self.state = GameState.IN_GAME
        if self.is_quickplay:
            self._setup_quickplay()
        self.turn_start_time = time.time()

    def _setup_quickplay(self):
        # Điền ngẫu nhiên 30% số cạnh
        possible_moves = self.board.get_possible_moves()
        num_moves_to_make = int(len(possible_moves) * 0.3)
        moves_to_make = random.sample(possible_moves, num_moves_to_make)
        
        # Cứ thay phiên 1-2 để đánh dấu
        player = 1
        for move in moves_to_make:
            score = self.board.make_move(move, player)
            if score == 0:
                player = 3 - player

    def update(self):
        if self.state == GameState.IN_GAME and self.is_quickplay:
            if time.time() - self.turn_start_time > self.turn_time_limit:
                # Hết giờ -> tự động đi nước đi đầu tiên có thể và đổi lượt
                moves = self.board.get_possible_moves()
                if moves:
                    self.make_move(moves[0])

    def make_move(self, move):
        if self.state != GameState.IN_GAME:
            return None

        score = self.board.make_move(move, self.current_player)

        # Nếu không ăn được điểm thì đổi lượt
        if score == 0:
            self.current_player = 3 - self.current_player # 1 -> 2, 2 -> 1

        self.turn_start_time = time.time() # Reset timer
        self._check_game_over()
        return score

    def _check_game_over(self):
        if self.board.is_game_over():
            p1_score = self.board.get_score(1)
            p2_score = self.board.get_score(2)
            
            if p1_score > p2_score:
                self.state = GameState.PLAYER_1_WIN
            elif p2_score > p1_score:
                self.state = GameState.PLAYER_2_WIN
            else:
                self.state = GameState.DRAW
