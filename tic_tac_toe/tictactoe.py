import os
from .board import Board

class TicTacToe:
  def __init__(self):
    self.game = Board()

  def display_logo(self) -> None:
    logo_path = os.path.join(os.path.dirname(__file__), "logo.txt")
    try:
      with open(logo_path, "r") as file:
        logo = file.read()
      print(logo)
    except FileNotFoundError:
      pass

  def start(self) -> None:
    self.display_logo()
    host, port = input('Specify the host and port:\n').split()
    self.game.connect_to_game(host, int(port))

if __name__ == "__main__":
  TicTacToe().start()