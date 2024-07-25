class Board:
    def __init__(self):
        self.board = [[False for _ in range(7)] for _ in range(7)]
        self.SHIP_MIN_SIZE = 2
        self.SHIP_MAX_SIZE = 5


    def __str__(self) -> str:
        return ''.join('1' if cell else '0' for row in self.board for cell in row)


    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return str(self) == str(other)


    def display(self) -> None:
        print("  A B C D E F G")
        for i, row in enumerate(self.board):
            print(7 - i, end=" ")
            for j, ship_piece in enumerate(row):
                print('■' if ship_piece else ' ', end=" ")
            print(7 - i)
        print("  A B C D E F G")


    def display_bombed(self) -> None:
        print("  A B C D E F G")
        for i, row in enumerate(self.board):
            print(7 - i, end=" ")
            for j, bomb in enumerate(row):
                end_value = "" if bomb == "\U0001F4A5" else " "
                print(bomb if bomb else ' ', end=end_value)
            print(7 - i)
        print("  A B C D E F G")


    def is_within_bounds(self, position: str) -> bool:
        if len(position) != 2:
            return False
        col = position[0].upper()
        row = position[1]
        
        if col < 'A' or col > 'G':
            return False
        if not row.isdigit() or int(row) < 1 or int(row) > 7:
            return False
        
        return True


    def transform_coordinate(self, position: str) -> tuple[int, int]:
        row = 7 - int(position[1])
        col = ord(position[0].upper()) - ord('A')
        return row, col


    def is_valid_ship_placement(self, start: str, end: str) -> bool:
        if not (self.is_within_bounds(start) and self.is_within_bounds(end)):
            return False

        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)

        if start_row != end_row and start_col != end_col:
            return False  # Not in a straight line

        length = abs(start_row - end_row) + 1 if start_col == end_col else abs(start_col - end_col) + 1

        if length < self.SHIP_MIN_SIZE or length > self.SHIP_MAX_SIZE:
            return False

        # Check for existing ship pieces in the path
        if start_row == end_row:
            for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                if self.board[start_row][col]:
                    return False
        else:
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                if self.board[row][start_col]:
                    return False

        return True


    def place_ship(self, start: str, end: str) -> None:
        if not self.is_valid_ship_placement(start, end):
            return

        start_row, start_col = self.transform_coordinate(start)
        end_row, end_col = self.transform_coordinate(end)

        if start_row == end_row:
            for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                self.board[start_row][col] = True
        else:
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                self.board[row][start_col] = True


    def is_valid_coordinate_to_bomb(self, coordinate: str) -> bool:
        row, col = self.transform_coordinate(coordinate)
        return self.is_within_bounds(coordinate) and not self.board[row][col]
        

    def is_valid_bombing(self, coordinate: str) -> bool:
        row, col = self.transform_coordinate(coordinate)
        return self.board[row][col]
        

    def bomb(self, coordinate: str, symbol: str) -> None:
        row, col = self.transform_coordinate(coordinate)
        self.board[row][col] = symbol
        

    def is_all_bombed(self, str_other: str) -> bool:
        str_self = str(self)
        
        for s1, s2 in zip(str_self, str_other):
            if s1 == '1' and s2 != '1':
                return False
        return True


if __name__ == "__main__":
    board = Board()
    board.display()
    print(str(board))
