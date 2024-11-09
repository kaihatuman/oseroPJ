from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 現在のファイルの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# 静的ファイルのマウント
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ルートパスへのアクセスでindex.htmlを返す
@app.get("/")
async def read_index():
    index_path = os.path.join(FRONTEND_DIR, 'index.html')
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)

class Move(BaseModel):
    row: int
    col: int

class Othello:
    def __init__(self):
        # 8x8 のボードを初期化（' 'は空のセル）
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # 初期配置（中央の4つの石をセット）
        self.board[3][3] = self.board[4][4] = 'O'
        self.board[3][4] = self.board[4][3] = 'X'
        # 初期プレイヤーは'X'
        self.current_player = 'X'

    def is_valid_move(self, row, col):
        """指定された位置に手が打てるか確認する"""
        if self.board[row][col] != ' ':
            return False  # すでに石が置かれている場所は無効
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
        """指定された場所に石を置いた後、挟んだ相手の石をひっくり返す"""
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
        """指定された位置に手を打つ"""
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        self.flip_discs(row, col)
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def has_valid_move(self):
        """現在のプレイヤーが打てる手があるかチェック"""
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

    def get_valid_moves(self):
        """有効な手の一覧を取得"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    valid_moves.append({"row": row, "col": col})
        return valid_moves

game = Othello()

@app.get("/board")
def get_board():
    return {
        "board": game.board,
        "current_player": game.current_player,
        "valid_moves": game.get_valid_moves()
    }

@app.post("/move")
def make_move(move: Move):
    if not (0 <= move.row < 8 and 0 <= move.col < 8):
        raise HTTPException(status_code=400, detail="無効な座標です")
    
    if not game.make_move(move.row, move.col):
        raise HTTPException(status_code=400, detail="その場所には置けません")
    
    return get_board()

@app.get("/status")
def game_status():
    return {"winner": game.get_winner()}

@app.post("/restart")
def restart_game():
    global game
    game = Othello()
    return get_board()

if __name__ == '__main__':
    import uvicorn
    print(f"Frontend directory: {FRONTEND_DIR}")
    print(f"Index file path: {os.path.join(FRONTEND_DIR, 'index.html')}")
    uvicorn.run(app, host="0.0.0.0", port=8000)