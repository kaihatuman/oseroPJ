from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ゲームのロジックを管理するクラス
class Othello:
    def __init__(self):
        # 8x8 のボードを初期化（' 'は空のセル）
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # 初期配置（中央の4つの石をセット）
        self.board[3][3] = self.board[4][4] = 'O'
        self.board[3][4] = self.board[4][3] = 'X'
        # 初期プレイヤーは'X'
        self.current_player = 'X'

    def print_board(self):
        """ボードを文字列として表示"""
        return '\n'.join(' '.join(row) for row in self.board)

    def is_valid_move(self, row, col):
        """指定された位置に手が打てるか確認する"""
        if self.board[row][col] != ' ':
            return False  # すでに石が置かれている場所は無効
        opponent = 'O' if self.current_player == 'X' else 'X'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            # 相手の石を挟むかどうかを調べる
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                r, c = r + dr, c + dc
                found_opponent = True
            # 最後に自分の石があれば、その方向に相手の石を挟めたことになる
            if found_opponent and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                return True
        return False

    def flip_discs(self, row, col):
        """指定された場所に石を置いた後、挟んだ相手の石をひっくり返す"""
        opponent = 'O' if self.current_player == 'X' else 'X'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            discs_to_flip = []
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == opponent:
                discs_to_flip.append((r, c))
                r, c = r + dr, c + dc
            # 挟んだ相手の石をひっくり返す
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for rr, cc in discs_to_flip:
                    self.board[rr][cc] = self.current_player

    def make_move(self, row, col):
        """指定された位置に手を打つ"""
        if not self.is_valid_move(row, col):
            return False  # 無効な手の場合はFalseを返す
        self.board[row][col] = self.current_player
        self.flip_discs(row, col)
        # プレイヤーを交代
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def has_valid_move(self):
        """どちらかのプレイヤーに有効な手があるかを確認"""
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    return True
        return False

    def get_winner(self):
        """ゲーム終了後の勝者を判定"""
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        if x_count > o_count:
            return 'X (黒)'
        elif o_count > x_count:
            return 'O (白)'
        else:
            return '引き分け'

# ゲームオブジェクトの作成
game = Othello()

# プレイヤーの手を受け取るためのモデル
class Move(BaseModel):
    row: int
    col: int

@app.get("/")
def home():
    # ホームにアクセスすると、ボードと現在のプレイヤー情報を返す
    return {"board": game.board, "current_player": game.current_player}

@app.get("/board")
def get_board():
    return {"board": game.board, "current_player": game.current_player}

# プレイヤーが手を打つ処理
@app.post("/move")
def make_move(move: Move):
    if game.make_move(move.row, move.col):
        return {"board": game.board, "current_player": game.current_player, "valid": True}
    else:
        return {"valid": False, "message": "無効な手です。"}, 400

# ゲーム終了時の勝者を取得
@app.get("/status")
def game_status():
    return {"status": game.get_winner()}

# ゲームをリスタートする処理
@app.post("/restart")
def restart_game():
    global game
    game = Othello()  # 新しいゲームを開始
    return {"message": "ゲームがリスタートされました"}

# サーバーを起動するためのコードは以下で実行されます。
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
