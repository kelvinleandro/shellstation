from typing import Union
from .pieces import *


class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.__pieces = {
            "pawn": Pawn,
            "king": King,
            "queen": Queen,
            "rook": Rook,
            "bishop": Bishop,
            "knight": Knight,
        }
    

    def setup_board(self) -> None:
        # Setup blue pieces (assuming blue is for one player and red is for the other)
        for i in range(8):
            self.board[1][i] = Pawn('blue')
        self.board[0][0] = Rook('blue')
        self.board[0][1] = Knight('blue')
        self.board[0][2] = Bishop('blue')
        self.board[0][3] = Queen('blue')
        self.board[0][4] = King('blue')
        self.board[0][5] = Bishop('blue')
        self.board[0][6] = Knight('blue')
        self.board[0][7] = Rook('blue')
    
        # Setup red pieces
        for i in range(8):
            self.board[6][i] = Pawn('red')
        self.board[7][0] = Rook('red')
        self.board[7][1] = Knight('red')
        self.board[7][2] = Bishop('red')
        self.board[7][3] = Queen('red')
        self.board[7][4] = King('red')
        self.board[7][5] = Bishop('red')
        self.board[7][6] = Knight('red')
        self.board[7][7] = Rook('red')
    
    
    def display(self) -> None:
        print('  A B C D E F G H')
        for i in range(8):
            row = str(8 - i) + ' '
            for j in range(8):
                piece = self.board[i][j]
                row += str(piece) + ' ' if piece != ' ' else '. '
            print(row + str(8 - i))
        print('  A B C D E F G H')
    

    def display_inverted(self) -> None:
        print('  H G F E D C B A')
        for i in range(8):
            row = str(i + 1) + ' '
            for j in range(7, -1, -1):
                piece = self.board[7 - i][j]
                row += str(piece) + ' ' if piece != ' ' else '. '
            print(row + str(i + 1))
        print('  H G F E D C B A')


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


    def get_piece(self, position: str) -> Union['ChessPiece', str]:
        row, col = self.transform_coordinate(position)
        return self.board[row][col]


    def is_valid_move(self, start: str, end: str) -> bool:
        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == ' ':
            return False

        if target != ' ' and target.color == piece.color:
            return False

        col_diff = abs(start_col - end_col)
        row_diff = abs(start_row - end_row)

        if isinstance(piece, Pawn):
            if piece.color == 'blue':
                if start_row == 1 and end_row == start_row + 2 and col_diff == 0 and target == ' ':
                    return True
                if end_row == start_row + 1 and col_diff == 0 and target == ' ':
                    return True
                if end_row == start_row + 1 and col_diff == 1 and target != ' ' and target.color != piece.color:
                    return True
            else:
                if start_row == 6 and end_row == start_row - 2 and col_diff == 0 and target == ' ':
                    return True
                if end_row == start_row - 1 and col_diff == 0 and target == ' ':
                    return True
                if end_row == start_row - 1 and col_diff == 1 and target != ' ' and target.color != piece.color:
                    return True

        if isinstance(piece, Rook):
            if col_diff == 0 or row_diff == 0:
                if self.is_clear_path(start_row, start_col, end_row, end_col):
                    return True

        if isinstance(piece, Knight):
            if (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2):
                return True

        if isinstance(piece, Bishop):
            if col_diff == row_diff:
                if self.is_clear_path(start_row, start_col, end_row, end_col):
                    return True

        if isinstance(piece, Queen):
            if col_diff == row_diff or col_diff == 0 or row_diff == 0:
                if self.is_clear_path(start_row, start_col, end_row, end_col):
                    return True
        
        if isinstance(piece, King):
            if col_diff <= 1 and row_diff <= 1:
                return True

        return False


    def is_clear_path(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
        step_col = (end_col - start_col) // max(1, abs(end_col - start_col))

        current_row, current_col = start_row + step_row, start_col + step_col
        while current_row != end_row or current_col != end_col:
            if self.board[current_row][current_col] != ' ':
                return False
            current_row += step_row
            current_col += step_col

        return True


    def move_piece(self, start: str, end: str) -> None:
        if self.is_valid_move(start, end):
            start_row, start_col = self.transform_coordinate(start)
            end_row, end_col = self.transform_coordinate(end)

            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = ' '
            print(f"Moved from {start} to {end}")
        else:
            print(f"Invalid move from {start} to {end}")


    def transform_coordinate(self, position: str) -> tuple[int, int]:
        row = 8 - int(position[1])
        col = ord(position[0].upper()) - ord('A')
        return row, col


    def is_promotion(self, position: str) -> bool:
        piece = self.get_piece(position)

        if isinstance(piece, Pawn) and piece.color == "blue":
            return int(position[1]) == 1
        elif isinstance(piece, Pawn) and piece.color == "red":
            return int(position[1]) == 8
        return False

    
    def replace_piece(self, position: str, piece: str, color: str) -> None:
        row, col = self.transform_coordinate(position)
        self.board[row][col] = self.__pieces.get(piece)(color)
        
    
if __name__ == "__main__":
    board = Board()
    board.display()
    # board.display_inverted() # other player POV
    
    print("\nMove to A2 to A3\n")
    board.move_piece("A2","A3")
    board.display()

    print("\nInvalid move A3 to A5\n")
    board.move_piece('A3', 'A5')
    board.display()

    print("\nGet piece at A3\n")
    piece = board.get_piece('A3')
    print(f"Piece at A3: {piece}")
