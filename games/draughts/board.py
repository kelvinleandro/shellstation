from typing import Union
from .piece import Piece


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
                    print('■' if (i + j) % 2 == 0 else ' ', end=" ")
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
                    print('■' if (i + j) % 2 == 0 else ' ', end=" ")
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


    def is_valid_move(self, moves: list[str]) -> bool:
        n_movements = len(moves) - 1
        if n_movements < 1:
            return False
        
        if not all(self.is_within_bounds(move) for move in moves):
            return False

        piece = self.get_piece(moves[0])
        if piece is None:
            return False

        n_captures = 0
        for i in range(1, len(moves)):
            start, end = moves[i-1], moves[i]
            if not self.is_valid_single_move(piece, start, end):
                return False
            n_captures += int(self.is_capture_move(piece, start, end))

        # If the sequence is longer than one move, ensure all are captures
        if n_movements > 1 and n_captures != n_movements:
            return False

        return True


    def is_valid_single_move(self, piece: Piece, start: str, end: str) -> bool:
        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if self.get_piece(end) is not None:
            return False

        if piece.king:
            if abs(row_diff) == abs(col_diff):
                step_row = 1 if end_row > start_row else -1
                step_col = 1 if end_col > start_col else -1
                row, col = start_row + step_row, start_col + step_col
                opponent_pieces_encountered = 0
                while row != end_row and col != end_col:
                    current_piece = self.board[row][col]
                    if current_piece is not None:
                        if current_piece.color == piece.color:
                            return False  # Cannot jump over own pieces
                        opponent_pieces_encountered += 1
                    row += step_row
                    col += step_col
                return opponent_pieces_encountered <= 1
            return False

        # Regular pieces can move only forward diagonally one square or capture
        if abs(row_diff) == 1 and abs(col_diff) == 1:
            return True

        # Check for capturing move
        if abs(row_diff) == 2 and abs(col_diff) == 2:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            middle_piece = self.board[mid_row][mid_col]
            if middle_piece is not None and middle_piece.color != piece.color:
                return True

        return False


    def is_capture_move(self, piece: Piece, start: str, end: str) -> bool:
        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)
        if piece.king:
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            row, col = start_row + step_row, start_col + step_col
            opponent_pieces_encountered = 0
            while row != end_row and col != end_col:
                current_piece = self.board[row][col]
                if current_piece is not None and piece.color != current_piece.color:
                    opponent_pieces_encountered += 1
                row += step_row
                col += step_col
            return opponent_pieces_encountered == 1
        return abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2


    def move_piece(self, moves: list[str]) -> None:
        if not self.is_valid_move(moves):
            print("Invalid move")
            return

        start = moves[0]
        piece = self.get_piece(start)
        if piece is None:
            return

        for i in range(1, len(moves)):
            self.execute_single_move(piece, moves[i-1], moves[i])

        # Check for king promotion
        end = moves[-1]
        end_row, _ = self.transform_coordinate(end)
        if (piece.color == 'blue' and end_row == 7) or (piece.color == 'red' and end_row == 0):
            piece.make_king()


    def execute_single_move(self, piece: Piece, start: str, end: str) -> None:
        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)

        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1

        row, col = start_row + step_row, start_col + step_col
        while row != end_row and col != end_col:
            if self.board[row][col] is not None and self.board[row][col].color != piece.color:
                self.board[row][col] = None
            row += step_row
            col += step_col


if __name__ == "__main__":
    board = Board()
    board.display()
    # board.display_inverted()
    board.move_piece(['D6', 'C5'])
    board.move_piece(['C5', 'D4'])
    board.move_piece(['C7', 'D6'])
    board.move_piece(['C3', 'E5', 'C7'])
    board.move_piece(['B8', 'D6'])
    # board.move_piece(['C1', 'D2'])
    board.display()
