import socket
import threading
import os
from .board import Board

class Battleship:
    def __init__(self):
        self.board = Board()
        self.bombed_board = Board()
        self.turn = 1
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

        self.init_ships()

        if is_host:
            self.you = 1
            self.opponent = 2
            threading.Thread(target=self.handle_connection, args=(client,)).start()
            server.close()
        else:
            self.you = 2
            self.opponent = 1
            threading.Thread(target=self.handle_connection, args=(client,)).start()

    
    def init_ships(self) -> None:
        remaining_ships = 5

        while remaining_ships > 0:
            self.board.display()
            while True:
                print("Enter the coordinates where you want to place your ship (e.g. A1 A2)")
                print(f"Ship min size: {self.board.SHIP_MIN_SIZE}")
                print(f"Ship max size: {self.board.SHIP_MAX_SIZE}")
                ship_position = input(f"Coordinates: ").upper().strip()
                coordinates = ship_position.split()
                if len(coordinates) > 2 or not self.board.is_valid_ship_placement(*coordinates):
                    print("Invalid coordinates. Try again.")
                else:
                    self.board.place_ship(*coordinates)
                    break
            remaining_ships -= 1


    def start(self) -> None:
        self.display_logo()
        host, port = input('Specify the host and port:\n').split()
        self.connect_to_game(host, int(port))


    def handle_connection(self, client: socket.socket) -> None:
        while not self.game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Your board:")
            self.board.display()
            print("Your bomb board:")
            self.bombed_board.display_bombed()

            if self.turn == self.you:
                while True:
                    coordinate = input("Enter a coordinate to bomb or exit: ").strip().upper()
                    if coordinate == "EXIT":
                        client.send("EXIT".encode('utf-8'))
                        client.close()
                        self.game_over = True
                        break
                    elif len(coordinate.split()) > 1 or not self.bombed_board.is_valid_coordinate_to_bomb(coordinate):
                        print('Invalid coordinate! Try again.')
                    else:
                        client.send(f"VALIDATE_REQ {coordinate}".encode())

                        response = client.recv(1024).decode()
                        if response.startswith("VALIDATE_RES"):
                            self.bombed_board.bomb(coordinate, "\U0001F4A5" if response[-1] == "1" else "X")
                            self.turn = self.opponent
                            break
                        
            else:
                data = client.recv(1024)
                if not data: break
                
                message = data.decode()
                if message == "EXIT":
                    self.game_over = True
                    break
                elif message.startswith("VALIDATE_REQ"):
                    response = "1" if self.board.is_valid_bombing(message[13:]) else "0"
                    client.send(f"VALIDATE_RES {response}".encode())
                
                self.turn = self.you
            # self.update_game_over(client)
        print('GAME OVER.')


    def update_game_over(self, client: socket.socket) -> None:
        client.send(f"GAME_OVER_REQ {str(self.bombed_board)}".encode())
        message = client.recv(1024).decode()
        if message.startswith("GAME_OVER_RES"):
            self.game_over = message[-1] == "1"
        elif message.startswith("GAME_OVER_REQ"):
            other_board_str = message[14:]
            game_over = self.board.is_all_bombed(other_board_str)
            client.send(f"GAME_OVER_RES {'1' if game_over else '0'}".encode())


if __name__ == "__main__":
    Battleship().start()
