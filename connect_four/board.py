class Board:
    def __init__(self) -> None:
        self.board = [[None for _ in range(7)] for _ in range(6)]

    def apply_move(self, column: int, player: str) -> None:
        for row in reversed(range(6)):
            if self.board[row][column - 1] is None:
                self.board[row][column - 1] = player
                return

    def check_valid_move(self, column: int) -> bool:
        if column < 1 or column > 7:
            return False
        return any(self.board[row][column - 1] is None for row in range(6))

    def display(self) -> None:
        print("1   2   3   4   5   6   7 ")
        for row in self.board:
            print(" | ".join([' ' if cell is None else cell for cell in row]))
            print('-' * 29)
