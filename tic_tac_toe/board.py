class Board:
  def __init__(self) -> None:
    self.board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]

  def apply_move(self, move: list[str], player: str) -> None:
    self.board[int(move[0])][int(move[1])] = player

  def check_valid_move(self, move: list[str]) -> bool:
    row, column = int(move[0]), int(move[1])
    if row >= len(self.board) or row < 0 or column >= len(self.board[0]) or column < 0:
      return False
    return self.board[row][column] == " "

  def print_board(self) -> None:
    for row in range(3):
      print(" | ".join(self.board[row]))
      if row != 2:
        print('-'*15)
