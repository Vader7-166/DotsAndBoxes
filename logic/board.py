class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
        # True nếu cạnh đã được vẽ, False nếu chưa
        self.h_edges = [[False for _ in range(cols)] for _ in range(rows + 1)]
        self.v_edges = [[False for _ in range(cols + 1)] for _ in range(rows)]
        
        # Lưu lại người vẽ cạnh để có màu tương ứng
        self.h_edge_owners = [[0 for _ in range(cols)] for _ in range(rows + 1)]
        self.v_edge_owners = [[0 for _ in range(cols + 1)] for _ in range(rows)]
        
        # 0 nếu chưa có ai sở hữu, 1 cho P1, 2 cho P2
        self.boxes = [[0 for _ in range(cols)] for _ in range(rows)]
        
        self.p1_score = 0
        self.p2_score = 0

    def clone(self):
        """Tạo bản sao cực nhanh của bàn cờ thay vì dùng copy.deepcopy()"""
        new_board = Board(self.rows, self.cols)
        new_board.h_edges = [row[:] for row in self.h_edges]
        new_board.v_edges = [row[:] for row in self.v_edges]
        new_board.h_edge_owners = [row[:] for row in self.h_edge_owners]
        new_board.v_edge_owners = [row[:] for row in self.v_edge_owners]
        new_board.boxes = [row[:] for row in self.boxes]
        new_board.p1_score = self.p1_score
        new_board.p2_score = self.p2_score
        return new_board

    def get_possible_moves(self):
        moves = []
        for r in range(self.rows + 1):
            for c in range(self.cols):
                if not self.h_edges[r][c]:
                    moves.append(('h', r, c))
        for r in range(self.rows):
            for c in range(self.cols + 1):
                if not self.v_edges[r][c]:
                    moves.append(('v', r, c))
        return moves

    def make_move(self, move, player_id):
        direction, r, c = move
        if direction == 'h':
            self.h_edges[r][c] = True
            self.h_edge_owners[r][c] = player_id
        else:
            self.v_edges[r][c] = True
            self.v_edge_owners[r][c] = player_id

        # Kiểm tra xem có tạo thành ô vuông nào không
        score = 0
        
        if direction == 'h':
            # Kiểm tra ô bên trên
            if r > 0 and self._check_box(r - 1, c):
                self.boxes[r - 1][c] = player_id
                score += 1
            # Kiểm tra ô bên dưới
            if r < self.rows and self._check_box(r, c):
                self.boxes[r][c] = player_id
                score += 1
        else:
            # Kiểm tra ô bên trái
            if c > 0 and self._check_box(r, c - 1):
                self.boxes[r][c - 1] = player_id
                score += 1
            # Kiểm tra ô bên phải
            if c < self.cols and self._check_box(r, c):
                self.boxes[r][c] = player_id
                score += 1

        if player_id == 1:
            self.p1_score += score
        else:
            self.p2_score += score
            
        return score

    def _check_box(self, r, c):
        return (self.h_edges[r][c] and 
                self.h_edges[r+1][c] and 
                self.v_edges[r][c] and 
                self.v_edges[r][c+1])

    def is_game_over(self):
        return self.p1_score + self.p2_score == self.rows * self.cols

    def get_score(self, player_id):
        if player_id == 1:
            return self.p1_score
        return self.p2_score

    def get_box_sides_count(self, r, c):
        """Trả về số lượng cạnh đã được vẽ của ô (r, c)."""
        count = 0
        if self.h_edges[r][c]: count += 1
        if self.h_edges[r+1][c]: count += 1
        if self.v_edges[r][c]: count += 1
        if self.v_edges[r][c+1]: count += 1
        return count

    def get_all_box_side_counts(self):
        """Trả về danh sách số lượng cạnh của tất cả các ô."""
        counts = []
        for r in range(self.rows):
            for c in range(self.cols):
                counts.append(self.get_box_sides_count(r, c))
        return counts
