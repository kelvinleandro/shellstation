import socket
import threading
import os
from .board import Board

class Chess:
    def __init__(self):
        self.board = Board()
        self.turn = "red"
        self.you = "red"
        self.opponent = "blue"
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
            self.host_game(host, int(port))
            print(f"Hosting the game on {host}:{port}")
        elif player == 'player2':
            self.connect_to_game(host, int(port))
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
                    move = input("Enter a move (e.g., A2 A3): ").strip().upper()
                    coordinates = move.split()
                    if not self.board.is_within_bounds(coordinates[0]) or not self.board.is_within_bounds(coordinates[1]):
                        print('Invalid coordinates! Try again.')
                    elif self.board.get_piece(coordinates[0]) != " " and self.board.get_piece(coordinates[0]).color == self.opponent:
                        print('Invalid piece! Try again.')
                    elif self.board.is_valid_move(*coordinates):
                        self.board.move_piece(*coordinates)

                        if self.board.is_promotion(coordinates[1]):
                            print('PAWN PROMOTION!!!')
                            print('Choose the piece to which you\'d like to promote your pawn: Rook, Knight, Bishop or Queen.')
                            while True:
                                piece_option = input("Piece: ").strip().lower()
                                if piece_option not in ("rook", "knight", "bishop", "queen"):
                                    print(f"{piece_option} is an invalid option. Try again.")
                                else:
                                    break
                            
                            self.board.replace_piece(coordinates[1], piece_option, self.you)
                            client.send(f"promotion {move} {piece_option}".encode('utf-8'))
                        else:
                            client.send(move.encode('utf-8'))

                        self.turn = self.opponent
                        break
                    else:
                        print('Invalid move! Try again.')
            else:
                data = client.recv(1024)
                if data:
                    content = data.decode('utf-8')
                    if content.startswith('promotion'):
                        _, start, end, piece_option = content.split()
                        self.board.move_piece(start, end)
                        self.board.replace_piece(end, piece_option, self.opponent)
                    else:
                        self.board.move_piece(*content.split())
                    self.turn = self.you
                else:
                    break


if __name__ == "__main__":
    Chess().start()
