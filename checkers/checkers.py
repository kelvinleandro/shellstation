
import socket
import threading
import os
from board import Board

class Checkers:
    def __init__(self):
        self.board = Board()
        self.turn = "red"
        self.you = None
        self.opponent = None
        self.game_over = False

  
    def display_logo(self) -> None:
        logo_path = os.path.join(os.path.dirname(__file__), "logo.txt")
        try:
            with open(logo_path, "r") as file:
                logo = file.read()
            print(logo)
        except FileNotFoundError:
            pass


    def connect_to_game(self, host: str, port: int) -> None:
        is_host = False
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen(1)

            client, addr = server.accept()
            is_host = True
        except OSError as e:
            if e.errno == 10048:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((host, port))
            else:
                raise e

        if is_host:
            self.you = "red"
            self.opponent = "blue"
            threading.Thread(target=self.handle_connection, args=(client,)).start()
            server.close()
        else:
            self.you = "blue"
            self.opponent = "red"
            threading.Thread(target=self.handle_connection, args=(client,)).start()


    def start(self) -> None:
        self.display_logo()
        host, port = input('Specify the host and port:\n').split()
        self.connect_to_game(host, int(port))


    def handle_connection(self, client: socket.socket) -> None:
        while not self.game_over:
            if self.you == "red":
                self.board.display()
            else:
                self.board.display_inverted()
            
            if self.turn == self.you:
                pass
            else:
                pass


if __name__ == "__main__":
    Checkers().start()
