class Piece:
    def __init__(self, color):
        self.color = color
        self.king = False  # Checkers piece starts as non-king

    def make_king(self):
        self.king = True

    @property
    def symbol(self):
        return '\u25CF' if not self.king else '♔'  # Circle for normal, crown for king

    @property
    def color_code(self):
        return '34' if self.color == 'blue' else '31'

    def __str__(self):
        return f"\033[{self.color_code}m{self.symbol}\033[0m"
