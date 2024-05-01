from dataclasses import dataclass
import inquirer
import argparse
from hangman.hangman import Hangman
from tic_tac_toe.tictactoe import TicTacToe


@dataclass
class ShellStation:
  games = {'Hangman': Hangman, 'TicTacToe': TicTacToe}


  def display_logo(self):
    with open("logo.txt", "r") as file:
      logo = file.read()
    print(logo)
  

  def start(self, game_name=None):
    if game_name:
      game_class = self.games.get(game_name)
      if game_class:
        game_class().start()
    else:
      self.display_logo()
      print('Welcome to ShellStation!')
      choice = inquirer.list_input("Select the game you wanna play", choices=self.games.keys())
      self.games[choice]().start()


def parse_arguments():
  parser = argparse.ArgumentParser(description="Run a specific game directly from the ShellStation game suite.")
  valid_games = ['Hangman', 'TicTacToe']
  parser.add_argument('-g', '--game', type=str, choices=valid_games,
                      help="Specify the game to play.")
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_arguments()
  shell_station = ShellStation()
  if args.game:
    shell_station.start(game_name=args.game)
  else:
    shell_station.start()
