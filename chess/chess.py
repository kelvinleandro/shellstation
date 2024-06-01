import socket
import threading
import os
from .board import Board

class Chess:
  def __init__(self) -> None:
    self.board = Board()
    self.turn = "red"
    self.you = "red"
    self.opponent = "blue"
    self.winner = None
    self.game_over = False

  
  def display_logo(self) -> None:
    logo_path = os.path.join(os.path.dirname(__file__), "logo.txt")
    try:
      with open(logo_path, "r") as file:
        logo = file.read()
      print(logo)
    except FileNotFoundError:
      pass


  def host_game(self, host: str, port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    client, addr = server.accept()
    self.you = "red"
    self.opponent = "blue"
    threading.Thread(target=self.handle_connection, args=(client,)).start()
    server.close()


  def connect_to_game(self, host: str, port: int) -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    self.you = "blue"
    self.opponent = "red"
    threading.Thread(target=self.handle_connection, args=(client,)).start()


  def start(self) -> None:
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


  def handle_connection(self, client: socket.socket) -> None:
    while not self.game_over:
      if self.you == "red":
        self.board.display()
      else:
        self.board.display_inverted()
      
      if self.turn == self.you:
        while True:
          move = input("Enter a move (e.g., A2 A3): ").upper()
          if self.board.validate_move(*move.split()):
            client.send(move.encode('utf-8'))
            self.board.move_piece(*move.split())
            self.turn = self.opponent
            break
          else:
            print('Invalid move!')
      else:
        data = client.recv(1024)
        if not data:
          break
        else:
          self.board.move_piece(*data.decode('utf-8').split())
          self.turn = self.you


if __name__ == "__main__":
  Chess().start()