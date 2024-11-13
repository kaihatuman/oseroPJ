
from tests.utils.board_helper import BoardHelper
from backend.othello import Othello

# テスト用のボードを作成
game = Othello()
helper = BoardHelper()

# カスタム盤面をテスト
test_board = """
--------
--OX----
--XO----
--------
--------
--------
--------
--------
"""

# 盤面をセット
game.board = helper.create_board_from_string(test_board)

# 盤面を表示
helper.print_board(game.board, game.current_player)

# 有効な手を確認
for row in range(8):
    for col in range(8):
        if game.is_valid_move(row, col):
            print(f"有効な手: ({row}, {col})")