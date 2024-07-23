class ChessPiece:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"\033[{self.color_code}m{self.symbol}\033[0m"

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K'
        self.color_code = '34' if color == 'blue' else '31'

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q'
        self.color_code = '34' if color == 'blue' else '31'

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R'
        self.color_code = '34' if color == 'blue' else '31'

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B'
        self.color_code = '34' if color == 'blue' else '31'

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N'
        self.color_code = '34' if color == 'blue' else '31'

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P'
        self.color_code = '34' if color == 'blue' else '31'

# Example usage
if __name__ == "__main__":
    blue_king = King('blue')
    red_queen = Queen('red')
    print(blue_king)
    print(red_queen)
