import random
import math
import time

class AIBot:
    def __init__(self, difficulty='medium', player_id=2):
        self.difficulty = difficulty
        self.player_id = player_id
        self.search_start_time = 0
        self.time_limit = 3.0 # Max seconds to think
        self.interrupted = False

    def get_move(self, board):
        possible_moves = board.get_possible_moves()
        if not possible_moves: return None
        if self.difficulty == 'easy': return self._get_easy_move(board)

        # Move Ordering for the top level
        ordered_moves = self._order_moves(board, possible_moves)
        
        target_depth = 4 if self.difficulty == 'medium' else 10
        if len(possible_moves) > 50: target_depth = min(target_depth, 3)
        
        self.search_start_time = time.time()
        self.interrupted = False
        
        best_move = ordered_moves[0]
        
        # Iterative Deepening
        for depth in range(1, target_depth + 1):
            move, val = self._get_best_move_at_depth(board, depth, ordered_moves)
            if not self.interrupted:
                best_move = move
            else:
                break # Stop if time ran out during this depth
            
            # If we already found a perfect win or it's taking too long, stop
            if val > 5000: break # Found a winning sequence
            if time.time() - self.search_start_time > self.time_limit: break

        return best_move

    def _get_best_move_at_depth(self, board, depth, ordered_moves):
        best_move = ordered_moves[0]
        best_val = -math.inf
        alpha = -math.inf
        beta = math.inf
        
        for move in ordered_moves:
            if time.time() - self.search_start_time > self.time_limit:
                self.interrupted = True
                return best_move, best_val
                
            sim_board = board.clone()
            score_gained = sim_board.make_move(move, self.player_id)
            is_bot_turn_next = (score_gained > 0)
            
            val = self._minimax(sim_board, depth - 1, alpha, beta, is_bot_turn_next)
            val += score_gained * 100
            
            if val > best_val:
                best_val = val
                best_move = move
            
            alpha = max(alpha, best_val)
            if beta <= alpha: break
            
        return best_move, best_val

    def _get_easy_move(self, board):
        possible_moves = board.get_possible_moves()
        for move in possible_moves:
            if board.clone().make_move(move, self.player_id) > 0: return move
        # Simple safe move check for easy
        safe_moves = []
        for m in possible_moves:
            sim = board.clone()
            sim.make_move(m, self.player_id)
            if not self._gives_opponent_score_internal(sim):
                safe_moves.append(m)
        return random.choice(safe_moves) if safe_moves else random.choice(possible_moves)

    def _gives_opponent_score_internal(self, board):
        opponent_id = 3 - self.player_id
        for m in board.get_possible_moves():
            if board.clone().make_move(m, opponent_id) > 0: return True
        return False

    def _order_moves(self, board, moves):
        def move_priority(move):
            direction, r, c = move
            completes = 0
            if direction == 'h':
                if r > 0 and board.get_box_sides_count(r-1, c) == 3: completes += 1
                if r < board.rows and board.get_box_sides_count(r, c) == 3: completes += 1
            else:
                if c > 0 and board.get_box_sides_count(r, c-1) == 3: completes += 1
                if c < board.cols and board.get_box_sides_count(r, c) == 3: completes += 1
            if completes > 0: return 100
            
            creates_three = False
            if direction == 'h':
                if r > 0 and board.get_box_sides_count(r-1, c) == 2: creates_three = True
                if r < board.rows and board.get_box_sides_count(r, c) == 2: creates_three = True
            else:
                if c > 0 and board.get_box_sides_count(r, c-1) == 2: creates_three = True
                if c < board.cols and board.get_box_sides_count(r, c) == 2: creates_three = True
            if creates_three: return -50
            return 0
        return sorted(moves, key=move_priority, reverse=True)

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        if time.time() - self.search_start_time > self.time_limit:
            self.interrupted = True
            return 0
            
        if depth == 0 or board.is_game_over():
            return self._evaluate_state(board)

        possible_moves = board.get_possible_moves()
        if is_maximizing:
            max_eval = -math.inf
            for move in possible_moves:
                sim = board.clone()
                score = sim.make_move(move, self.player_id)
                eval_val = self._minimax(sim, depth - 1, alpha, beta, score > 0) + score * 100
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha or self.interrupted: break
            return max_eval
        else:
            min_eval = math.inf
            opp_id = 3 - self.player_id
            for move in possible_moves:
                sim = board.clone()
                score = sim.make_move(move, opp_id)
                eval_val = self._minimax(sim, depth - 1, alpha, beta, not (score > 0)) - score * 100
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha or self.interrupted: break
            return min_eval

    def _evaluate_state(self, board):
        opponent_id = 3 - self.player_id
        score_diff = board.get_score(self.player_id) - board.get_score(opponent_id)
        counts = board.get_all_box_side_counts()
        return score_diff * 100 - counts.count(2) * 15 + counts.count(3) * 20
