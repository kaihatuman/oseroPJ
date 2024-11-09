class Othello:
    def __init__(self):
        # ボードの初期化：8x8の二次元リスト
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # 初期の4つの石を配置
        self.board[3][3] = self.board[4][4] = 'O'  # 白
        self.board[3][4] = self.board[4][3] = 'X'  # 黒
        self.current_player = 'X'  # 最初のプレイヤーは黒

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(f"{i} " + ' '.join(row))

    def is_valid_move(self, row, col):
        if self.board[row][col] != ' ':
            return False
        opponent = 'O' if self.current_player == 'X' else 'X'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                r, c = r + dr, c + dc
                found_opponent = True
            if found_opponent and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                return True
        return False

    def flip_discs(self, row, col):
        opponent = 'O' if self.current_player == 'X' else 'X'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            discs_to_flip = []
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                discs_to_flip.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for rr, cc in discs_to_flip:
                    self.board[rr][cc] = self.current_player

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            print("無効な手です。再度入力してください。")
            return False
        self.board[row][col] = self.current_player
        self.flip_discs(row, col)
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def has_valid_move(self):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    return True
        return False

    def get_winner(self):
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        if x_count > o_count:
            return 'X (黒)'
        elif o_count > x_count:
            return 'O (白)'
        else:
            return '引き分け'

# ゲームの開始
game = Othello()
while game.has_valid_move():
    game.print_board()
    row = int(input(f"プレイヤー {game.current_player} - 行を選択 (0-7): "))
    col = int(input(f"プレイヤー {game.current_player} - 列を選択 (0-7): "))
    if game.make_move(row, col):
        print("\nターン交代\n")

game.print_board()
print(f"ゲーム終了！勝者: {game.get_winner()}")
