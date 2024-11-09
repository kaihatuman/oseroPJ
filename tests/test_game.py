
import pytest
from backend.othello import Othello
from .utils.board_helper import BoardHelper

class TestOthello:
    def setup_method(self):
        """各テストの前に実行される"""
        self.game = Othello()
        self.helper = BoardHelper()

    @pytest.fixture
    def initial_board(self):
        """初期盤面を提供するフィクスチャ"""
        return """
        --------
        --------
        --------
        ---OX---
        ---XO---
        --------
        --------
        --------
        """

    @pytest.fixture
    def mid_game_board(self):
        """中盤の盤面を提供するフィクスチャ"""
        return """
        --------
        --OX----
        --XO----
        --XO----
        --OX----
        --------
        --------
        --------
        """

    def test_initial_board(self, initial_board):
        """初期盤面のテスト"""
        self.game.board = self.helper.create_board_from_string(initial_board)
        assert self.game.board[3][3] == 'O'
        assert self.game.board[3][4] == 'X'
        assert self.game.board[4][3] == 'X'
        assert self.game.board[4][4] == 'O'

    def test_valid_moves(self, initial_board):
        """有効な手のテスト"""
        self.game.board = self.helper.create_board_from_string(initial_board)
        self.game.current_player = 'X'
        valid_moves = [
            (2, 3), (3, 2), (4, 5), (5, 4)
        ]
        for row, col in valid_moves:
            assert self.game.is_valid_move(row, col)

    def test_make_move(self, initial_board):
        """手を打つテスト"""
        self.game.board = self.helper.create_board_from_string(initial_board)
        self.game.current_player = 'X'
        assert self.game.make_move(2, 3)
        assert self.game.board[2][3] == 'X'
        assert self.game.board[3][3] == 'X'  # 石が裏返る

    def test_invalid_moves(self, initial_board):
        """無効な手のテスト"""
        self.game.board = self.helper.create_board_from_string(initial_board)
        invalid_moves = [
            (0, 0), (7, 7), (3, 3)  # 角、既に石がある場所
        ]
        for row, col in invalid_moves:
            assert not self.game.is_valid_move(row, col)