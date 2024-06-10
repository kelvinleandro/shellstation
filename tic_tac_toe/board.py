import socket
import threading

class Board:
  def __init__(self) -> None:
    self.board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
    self.turn = "X"
    self.you = None
    self.opponent = None
    self.winner = None
    self.game_over = False
    self.counter = 0


  def connect_to_game(self, host: str, port: int) -> None:
    is_host = False
    try:
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.bind((host, port))
      server.listen(1)

      client, addr = server.accept()
      is_host = True
    except OSError as e:
      if e.errno == 10048:  # Address already in use, attempt to connect as client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
      else:
        raise e

    if is_host:
      self.you = "X"
      self.opponent = "O"
      threading.Thread(target=self.handle_connection, args=(client,)).start()
      server.close()
    else:
      self.you = "O"
      self.opponent = "X"
      threading.Thread(target=self.handle_connection, args=(client,)).start()


  def handle_connection(self, client):
    while not self.game_over:
      if self.turn == self.you:
        while True:
          move = input("Enter a move (row,column): ")
          if self.check_valid_move(move.split(',')):
            client.send(move.encode('utf-8'))
            self.apply_move(move.split(','), self.you)
            self.turn = self.opponent
            break
          else:
            print('Invalid move!')
      else:
        data = client.recv(1024)
        if not data:
          break
        else:
          self.apply_move(data.decode('utf-8').split(','), self.opponent)
          self.turn = self.you


  def apply_move(self, move, player):
    if self.game_over: return

    self.counter += 1
    self.board[int(move[0])][int(move[1])] = player
    self.print_board()
    if self.check_if_won():
      if self.winner == self.you:
        print("You win")
        exit()
      elif self.winner == self.opponent:
        print("You lose")
        exit()
      else:
        if self.counter == 9:
          print("It is a tie.")
          exit()


  def check_valid_move(self, move):
    row, column = int(move[0]), int(move[1])
    if row >= len(self.board) or row < 0 or column >= len(self.board[0]) or column < 0:
      return False
    return self.board[row][column] == " "


  def check_if_won(self):
    for row in range(3):
      if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
        self.winner = self.board[row][0]
        self.game_over = True
        return True

    for column in range(3):
      if self.board[0][column] == self.board[1][column] == self.board[2][column] != " ":
        self.winner = self.board[0][column]
        self.game_over = True
        return True

    if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
      self.winner = self.board[0][0]
      self.game_over = True
      return True
      
    if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
      self.winner = self.board[0][2]
      self.game_over = True
      return True

    return False


  def print_board(self):
    for row in range(3):
      print(" | ".join(self.board[row]))
      if row != 2:
        print('-'*15)