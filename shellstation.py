from dataclasses import dataclass
import inquirer
from hangman.hangman import Hangman
from tic_tac_toe.tictactoe import TicTacToe


@dataclass
class ShellStation:
  games = [Hangman, TicTacToe]
  names = [Game.__name__ for Game in games]


  def display_logo(self):
    with open("logo.txt", "r") as file:
      logo = file.read()
    print(logo)
  

  def start(self):
    self.display_logo()
    print('Welcome to ShellStation!')
    choice = inquirer.list_input("Select the game you wanna play", choices=self.names)
    index = self.names.index(choice)
    self.games[index]().start() # initializes the selected game


if __name__ == "__main__":
  ShellStation().start()