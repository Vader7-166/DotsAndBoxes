import random
import math

class AIBot:
    def __init__(self, difficulty='medium', player_id=2):
        self.difficulty = difficulty
        self.player_id = player_id
        
        # Thiết lập độ sâu cho thuật toán Minimax dựa trên độ khó
        if self.difficulty == 'easy':
            self.max_depth = 1
        elif self.difficulty == 'medium':
            self.max_depth = 2 # Giảm depth để tránh bị treo game
        else: # hard
            self.max_depth = 4 # Tối ưu hóa lại thay vì 5 gây nghẽn

    def get_move(self, board):
        if self.difficulty == 'easy':
            return self._get_easy_move(board)
        else:
            return self._get_minimax_move(board)

    def _get_easy_move(self, board):
        possible_moves = board.get_possible_moves()
        if not possible_moves:
            return None

        safe_moves = []
        for move in possible_moves:
            simulated_board = board.clone()
            simulated_board.make_move(move, self.player_id)
            
            if not self._gives_opponent_score(simulated_board):
                safe_moves.append(move)

        if safe_moves:
            return random.choice(safe_moves)
        return random.choice(possible_moves)

    def _gives_opponent_score(self, board):
        opponent_id = 1 if self.player_id == 2 else 2
        possible_moves = board.get_possible_moves()
        
        for move in possible_moves:
            simulated_board = board.clone()
            score = simulated_board.make_move(move, opponent_id)
            if score > 0:
                return True
        return False

    def _get_minimax_move(self, board):
        best_move = None
        best_val = -math.inf
        alpha = -math.inf
        beta = math.inf
        
        possible_moves = board.get_possible_moves()
        if not possible_moves:
            return None

        # Giới hạn số nhánh tìm kiếm nếu bàn cờ quá lớn và trống để không bị lag (No response)
        # Chỉ giới hạn trong những lượt đầu tiên của màn 7x7
        if len(possible_moves) > 40: 
            return self._get_easy_move(board)

        # Trộn ngẫu nhiên nước đi trước khi duyệt để đa dạng hóa
        random.shuffle(possible_moves)

        for move in possible_moves:
            simulated_board = board.clone()
            score_gained = simulated_board.make_move(move, self.player_id)
            
            is_bot_turn_next = (score_gained > 0)
            
            move_val = self._minimax(simulated_board, self.max_depth - 1, alpha, beta, is_bot_turn_next)
            
            move_val += score_gained

            if move_val > best_val:
                best_val = move_val
                best_move = move

            alpha = max(alpha, best_val)
            if beta <= alpha:
                break # Pruning

        return best_move if best_move is not None else random.choice(possible_moves)

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self._evaluate_state(board)

        possible_moves = board.get_possible_moves()
        opponent_id = 1 if self.player_id == 2 else 2

        if is_maximizing:
            max_eval = -math.inf
            for move in possible_moves:
                simulated_board = board.clone()
                score_gained = simulated_board.make_move(move, self.player_id)
                
                is_still_maximizing = (score_gained > 0)
                
                eval_val = self._minimax(simulated_board, depth - 1, alpha, beta, is_still_maximizing)
                eval_val += score_gained
                
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for move in possible_moves:
                simulated_board = board.clone()
                score_gained = simulated_board.make_move(move, opponent_id)
                
                is_still_minimizing = (score_gained > 0)
                
                eval_val = self._minimax(simulated_board, depth - 1, alpha, beta, not is_still_minimizing)
                eval_val -= score_gained
                
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate_state(self, board):
        opponent_id = 1 if self.player_id == 2 else 2
        bot_score = board.get_score(self.player_id)
        opponent_score = board.get_score(opponent_id)
        
        evaluation = bot_score - opponent_score
        
        return evaluation
