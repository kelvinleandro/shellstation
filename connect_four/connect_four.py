import os
import socket
import threading
from .board import Board

class ConnectFour:
    def __init__(self):
        self.board = Board()
        self.turn = "\033[31m\u25CF\033[0m"
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
            self.you = "\033[31m\u25CF\033[0m" # red circle
            self.opponent = "\033[34m\u25CF\033[0m" # blue circle
            threading.Thread(target=self.handle_connection, args=(client,)).start()
            server.close()
        else:
            self.you = "\033[34m\u25CF\033[0m" # blue circle
            self.opponent = "\033[31m\u25CF\033[0m" # red circle
            threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client: socket.socket) -> None:
        while not self.game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.board.display()
            if self.turn == self.you:
                while True:
                    move = input("Enter a column (1-7): ")

                    try:
                        column = int(move)
                    except ValueError:
                        print('Invalid column! Try again.')
                        continue

                    if self.board.check_valid_move(column):
                        client.send(move.encode('utf-8'))
                        self.board.apply_move(column, self.you)
                        self.turn = self.opponent
                        break
                    else:
                        print('Invalid column! Try again.')
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    column = int(data.decode('utf-8'))
                    self.board.apply_move(column, self.opponent)
                    self.turn = self.you
            self.counter += 1
            self.update_game_over()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.board.display()
        if self.winner == self.you:
            print("You win")
        elif self.winner == self.opponent:
            print("You lose")
        elif self.counter == 42:
            print("It's a tie.")
        else:
            print("Game over.")

    def update_game_over(self) -> None:
        board = self.board.board

        # Check for horizontal win
        for row in range(6):
            for col in range(4):
                if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != None:
                    self.winner = board[row][col]
                    self.game_over = True
                    return

        # Check for vertical win
        for col in range(7):
            for row in range(3):
                if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != None:
                    self.winner = board[row][col]
                    self.game_over = True
                    return

        # Check for positively sloped diagonal win
        for row in range(3):
            for col in range(4):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != None:
                    self.winner = board[row][col]
                    self.game_over = True
                    return
                
        # Check for negatively sloped diagonal win
        for row in range(3):
            for col in range(4):
                if board[row + 3][col] == board[row + 2][col + 1] == board[row + 1][col + 2] == board[row][col + 3] != None:
                    self.winner = board[row + 3][col]
                    self.game_over = True
                    return
            
        # Check for a tie (board full)
        if self.counter == 42:
            self.game_over = True

if __name__ == "__main__":
    ConnectFour().start()