
class BoardHelper:
    @staticmethod
    def create_board_from_string(board_str: str) -> list:
        """文字列から盤面を作成する"""
        return [
            [cell for cell in row.strip()]
            for row in board_str.strip().split('\n')
            if row.strip()
        ]

    @staticmethod
    def board_to_string(board: list) -> str:
        """盤面を文字列に変換する"""
        return '\n'.join(''.join(row) for row in board)

    @staticmethod
    def print_board(board: list, current_player: str = None):
        """盤面を表示する"""
        print("\n  0 1 2 3 4 5 6 7")
        for i, row in enumerate(board):
            print(f"{i} {' '.join(row)}")
        if current_player:
            print(f"\nCurrent player: {current_player}")    