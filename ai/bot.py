import random
import copy
import math

class AIBot:
    def __init__(self, difficulty='medium', player_id=2):
        \"\"\"
        Khởi tạo AI Bot.
        :param difficulty: Mức độ khó ('easy', 'medium', 'hard')
        :param player_id: ID của người chơi mà Bot đại diện (thường là 2)
        \"\"\"
        self.difficulty = difficulty
        self.player_id = player_id
        
        # Thiết lập độ sâu cho thuật toán Minimax dựa trên độ khó
        if self.difficulty == 'easy':
            self.max_depth = 1
        elif self.difficulty == 'medium':
            self.max_depth = 3
        else: # hard
            self.max_depth = 5

    def get_move(self, board):
        \"\"\"
        Hàm chính được gọi để lấy nước đi từ Bot.
        :param board: Đối tượng Board hiện tại
        :return: Nước đi (edge) được chọn
        \"\"\"
        if self.difficulty == 'easy':
            return self._get_easy_move(board)
        else:
            return self._get_minimax_move(board)

    def _get_easy_move(self, board):
        \"\"\"
        Bot mức dễ: Nối cạnh ngẫu nhiên nhưng cố gắng tránh nối cạnh thứ 3 của một ô.
        (Tránh biếu không điểm cho đối thủ).
        \"\"\"
        possible_moves = board.get_possible_moves()
        if not possible_moves:
            return None

        safe_moves = []
        for move in possible_moves:
            # Giả lập nước đi
            simulated_board = copy.deepcopy(board)
            simulated_board.make_move(move, self.player_id)
            
            # Kiểm tra xem nước đi này có tạo ra ô nào có đúng 3 cạnh không
            # Giả định Nam có hàm `has_any_box_with_three_edges()`
            # Hoặc ta có thể tự kiểm tra bằng cách xem đối thủ có thể ăn điểm ngay sau nước đi này không
            if not self._gives_opponent_score(simulated_board):
                safe_moves.append(move)

        # Nếu có nước đi an toàn, chọn ngẫu nhiên trong đó. Nếu không, đành chọn ngẫu nhiên nước đi bất kỳ.
        if safe_moves:
            return random.choice(safe_moves)
        return random.choice(possible_moves)

    def _gives_opponent_score(self, board):
        \"\"\"
        Kiểm tra xem với trạng thái bàn cờ hiện tại, đối thủ có thể ăn điểm ngay trong lượt tiếp theo không.
        \"\"\"
        opponent_id = 1 if self.player_id == 2 else 2
        possible_moves = board.get_possible_moves()
        
        for move in possible_moves:
            simulated_board = copy.deepcopy(board)
            # Giả định make_move trả về số điểm ghi được
            score = simulated_board.make_move(move, opponent_id)
            if score > 0:
                return True
        return False

    def _get_minimax_move(self, board):
        \"\"\"
        Sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning.
        \"\"\"
        best_move = None
        best_val = -math.inf
        alpha = -math.inf
        beta = math.inf
        
        possible_moves = board.get_possible_moves()
        if not possible_moves:
            return None

        for move in possible_moves:
            simulated_board = copy.deepcopy(board)
            score_gained = simulated_board.make_move(move, self.player_id)
            
            # Nếu ăn được điểm, Bot được đi tiếp -> giữ nguyên lượt của Bot (is_maximizing = True)
            # Nếu không ăn được điểm, đổi lượt cho đối thủ (is_maximizing = False)
            is_bot_turn_next = (score_gained > 0)
            
            move_val = self._minimax(simulated_board, self.max_depth - 1, alpha, beta, is_bot_turn_next)
            
            # Cộng thêm điểm vừa ghi được vào giá trị đánh giá
            move_val += score_gained

            if move_val > best_val:
                best_val = move_val
                best_move = move

            alpha = max(alpha, best_val)
            if beta <= alpha:
                break # Pruning

        return best_move if best_move is not None else random.choice(possible_moves)

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        \"\"\"
        Thuật toán Minimax cốt lõi.
        \"\"\"
        if depth == 0 or board.is_game_over():
            return self._evaluate_state(board)

        possible_moves = board.get_possible_moves()
        opponent_id = 1 if self.player_id == 2 else 2

        if is_maximizing:
            max_eval = -math.inf
            for move in possible_moves:
                simulated_board = copy.deepcopy(board)
                score_gained = simulated_board.make_move(move, self.player_id)
                
                # Nếu ghi điểm, vẫn tiếp tục lượt của Bot
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
                simulated_board = copy.deepcopy(board)
                score_gained = simulated_board.make_move(move, opponent_id)
                
                # Nếu đối thủ ghi điểm, họ vẫn tiếp tục lượt (nghĩa là Bot vẫn chưa được đi)
                is_still_minimizing = (score_gained > 0)
                
                eval_val = self._minimax(simulated_board, depth - 1, alpha, beta, not is_still_minimizing)
                eval_val -= score_gained # Trừ đi điểm mà đối thủ ghi được
                
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate_state(self, board):
        \"\"\"
        Hàm Heuristic chấm điểm trạng thái bàn cờ hiện tại.
        :return: Điểm số đánh giá (Càng cao càng tốt cho Bot)
        \"\"\"
        # Hàm Heuristic cơ bản: (Điểm Bot) - (Điểm đối thủ)
        opponent_id = 1 if self.player_id == 2 else 2
        bot_score = board.get_score(self.player_id)
        opponent_score = board.get_score(opponent_id)
        
        evaluation = bot_score - opponent_score
        
        # Phần nâng cao (tùy chọn): Đánh giá số ô có 3 cạnh (nguy hiểm)
        # evaluation -= (số ô có 3 cạnh) * trọng_số
        
        return evaluation
