from typing import Union
from piece import Piece

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self) -> None:
        # Setup blue pieces
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece('blue')

        # Setup red pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece('red')

    def display(self) -> None:
        print("  A B C D E F G H")
        for i, row in enumerate(self.board):
            print(8 - i, end=" ")
            for j, cell in enumerate(row):
                if cell is None:
                    print('■' if (i + j) % 2 == 1 else ' ', end=" ")
                else:
                    print(cell, end=" ")
            print(8 - i)
        print("  A B C D E F G H")

    def display_inverted(self) -> None:
        print("  H G F E D C B A")
        for i, row in enumerate(reversed(self.board)):
            print(i + 1, end=" ")
            for j, cell in enumerate(reversed(row)):
                if cell is None:
                    print('■' if (i + j) % 2 == 1 else ' ', end=" ")
                else:
                    print(cell, end=" ")
            print(i + 1)
        print("  H G F E D C B A")

    def is_within_bounds(self, position: str) -> bool:
        if len(position) != 2:
            return False
        col = position[0].upper()
        row = position[1]
        
        if col < 'A' or col > 'H':
            return False
        if not row.isdigit() or int(row) < 1 or int(row) > 8:
            return False
        
        return True

    def get_piece(self, position: str) -> Union['Piece', None]:
        row, col = self.transform_coordinate(position)
        return self.board[row][col]

    def transform_coordinate(self, position: str) -> tuple[int, int]:
        row = 8 - int(position[1])
        col = ord(position[0].upper()) - ord('A')
        return row, col

    def is_valid_move(self) -> bool:
        pass

    def move_piece(self) -> None:
        pass

if __name__ == "__main__":
    board = Board()
    board.display()
    board.display_inverted()
