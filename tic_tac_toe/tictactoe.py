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


  def start(self):
    self.display_logo()
    player, host, port = input('Select the player (player1/player2), host, and port:\n').split()

    if player == 'player1':
      self.game.host_game(host, int(port))
      print(f"Hosting the game on {host}:{port}")
    elif player == 'player2':
      self.game.connect_to_game(host, int(port))
      print(f"Connecting to the game at {host}:{port}")
    else:
      raise ValueError("Invalid user. Use 'player1' or 'player2'.")


if __name__ == "__main__":
  TicTacToe().start()