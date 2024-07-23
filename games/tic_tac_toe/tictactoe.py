import os
import socket
import threading
from .board import Board

class TicTacToe:
  def __init__(self):
    self.board = Board()
    self.turn = "X"
    self.you = None
    self.opponent = None
    self.winner = None
    self.game_over = False
    self.counter = 0


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
    self.connect_to_game(host, int(port))


  def connect_to_game(self, host: str, port: int) -> None:
    is_host = False
    try:
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.bind((host, port))
      server.listen(1)
      print(f"Waiting for a connection on {host}:{port}...")
      client, addr = server.accept()
      is_host = True
      print(f"Connected by {addr}")
    except OSError:
      try:  # Address already in use, attempt to connect as client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connected to {host}:{port}")
      except Exception as e:
        print(f"Failed to connect to {host}:{port}. Exception: {e}")
    
    if is_host:
      self.you = "X"
      self.opponent = "O"
      threading.Thread(target=self.handle_connection, args=(client,)).start()
      server.close()
    else:
      self.you = "O"
      self.opponent = "X"
      threading.Thread(target=self.handle_connection, args=(client,)).start()


  def handle_connection(self, client: socket.socket) -> None:
    while not self.game_over:
      os.system('cls' if os.name == 'nt' else 'clear')
      self.board.print_board()
      if self.turn == self.you:
        while True:
          move = input("Enter a move (e.g., 0,0): ")
          if self.board.check_valid_move(move.split(',')):
            client.send(move.encode('utf-8'))
            self.board.apply_move(move.split(','), self.you)
            self.turn = self.opponent
            break
          else:
            print('Invalid move! Try again.')
      else:
        data = client.recv(1024)
        if not data:
          break
        else:
          self.board.apply_move(data.decode('utf-8').split(','), self.opponent)
          self.turn = self.you
      self.counter += 1
      self.update_game_over()
    if self.winner == self.you:
      print("You win")
    elif self.winner == self.opponent:
      print("You lose")
    elif self.counter == 9:
      print("It is a tie.")


  def update_game_over(self) -> None:
    board = self.board.board
    for row in range(3):
      if board[row][0] == board[row][1] == board[row][2] != " ":
        self.winner = board[row][0]
        self.game_over = True
        return

    for column in range(3):
      if board[0][column] == board[1][column] == board[2][column] != " ":
        self.winner = board[0][column]
        self.game_over = True
        return

    if board[0][0] == board[1][1] == board[2][2] != " ":
      self.winner = board[0][0]
      self.game_over = True
      return
      
    if board[0][2] == board[1][1] == board[2][0] != " ":
      self.winner = board[0][2]
      self.game_over = True
      return

    if self.counter == 9:
      self.game_over = True


if __name__ == "__main__":
  TicTacToe().start()
