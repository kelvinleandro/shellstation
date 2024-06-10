from dataclasses import dataclass, field
from typing import List
import socket
import threading
import os


@dataclass
class Hangman:
  you: str = "chooser"
  game_over: bool = False
  guessed: bool = False
  word: str = ""
  guessed_letters: List[str] = field(default_factory=list)
  guessed_words: List[str] = field(default_factory=list)
  tries: int = 6


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

      client, addr = server.accept()
      is_host = True
    except OSError as e:
      if e.errno == 10048:  # Address already in use, attempt to connect as client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
      else:
        raise e

    if is_host:
      self.you = "chooser"
      threading.Thread(target=self.handle_connection, args=(client,)).start()
      server.close()
    else:
      self.you = "guesser"
      threading.Thread(target=self.handle_connection, args=(client,)).start()


  def handle_connection(self, client: socket.socket) -> None:
    if self.you == "chooser":
      self.word = input("Choose a word to guess: ").upper().strip()
      client.send(self.word.encode('utf-8'))
      self.manage_game(client)
    else:
      print('Waiting for other player chooses the word...')
      self.word = client.recv(1024).decode('utf-8')
      if self.word:
        self.play(client)


  def manage_game(self, client: socket.socket) -> None:
    print('Waiting for the game to end...')
    while not self.game_over:
      message = client.recv(1024).decode('utf-8')
      if message == "OVER":
        self.game_over = True

    print(f"The game is over. The word was {self.word}")


  def play(self, client: socket.socket) -> None:
    word_completion = "_" * len(self.word)
    print("Let's play Hangman!")
    print(self.display_hangman(self.tries))
    print(word_completion)
    print("\n")
    while not self.guessed and self.tries > 0:
      guess = input("Please guess a letter or word: ").upper().strip()
      if len(guess) == 1 and guess.isalpha():
        if guess in self.guessed_letters:
          print(f"You already guessed the letter {guess}")
        elif guess not in self.word:
          print(f"{guess} is not in the word.")
          self.tries -= 1
          self.guessed_letters.append(guess)
        else:
          print(f"Good job, {guess} is in the word!")
          self.guessed_letters.append(guess)
          word_as_list = list(word_completion)
          indices = [i for i, letter in enumerate(self.word) if letter == guess]
          for index in indices:
            word_as_list[index] = guess
          word_completion = "".join(word_as_list)
          if "_" not in word_completion:
            self.guessed = True
      elif len(guess) == len(self.word) and guess.isalpha():
        if guess in self.guessed_words:
          print(f"You already guessed the word {guess}")
        elif guess != self.word:
          print(f"{guess} is not the word.")
          self.tries -= 1
          self.guessed_words.append(guess)
        else:
          self.guessed = True
          word_completion = self.word
      else:
        print("Not a valid guess.")
      print(self.display_hangman(self.tries))
      print(word_completion)
      print("\n")
    client.send("OVER".encode('utf-8'))
    if self.guessed:
      print("Congrats, you guessed the word! You win!")
    else:
      print(f"Sorry, you ran out of tries. The word was {self.word}.")


  def display_hangman(self, tries: int) -> str:
    stages = [  # final state: head, torso, both arms, and both legs
                """
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |     / \\
                    -
                """,
                # head, torso, both arms, and one leg
                """
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |     / 
                    -
                """,
                # head, torso, and both arms
                """
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |      
                    -
                """,
                # head, torso, and one arm
                """
                    --------
                    |      |
                    |      O
                    |     \\|
                    |      |
                    |     
                    -
                """,
                # head and torso
                """
                    --------
                    |      |
                    |      O
                    |      |
                    |      |
                    |     
                    -
                """,
                # head
                """
                    --------
                    |      |
                    |      O
                    |    
                    |      
                    |     
                    -
                """,
                # initial empty state
                """
                    --------
                    |      |
                    |      
                    |    
                    |      
                    |     
                    -
                """
    ]
    return stages[tries]
      

if __name__ == "__main__":
  Hangman().start()
