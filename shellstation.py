from dataclasses import dataclass
import inquirer
import argparse
import os
import sys

from hangman.hangman import Hangman
from tic_tac_toe.tictactoe import TicTacToe
from chess.chess import Chess
from draughts.draughts import Draughts
from connect_four.connect_four import ConnectFour

@dataclass
class ShellStation:
  games = {'hangman': Hangman, 'tictactoe': TicTacToe, 'chess': Chess, 'draughts': Draughts, 'connect4': ConnectFour}


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


def run_test(test):
  test_file = os.path.join('test', f'{test}_test.py')
  if not os.path.exists(test_file):
    print(f"Test file {test_file} does not exist.")
    sys.exit(1)
  # Run the test file
  os.system(f'python {test_file}')


def parse_arguments():
  parser = argparse.ArgumentParser(description="Run a specific game or test directly from the ShellStation game suite.")
  valid_games = ['hangman', 'tictactoe', 'chess', 'draughts', 'connect4']
  group = parser.add_mutually_exclusive_group()
  group.add_argument('-g', '--game', type=str, choices=valid_games, help="Specify the game to play.")
  group.add_argument('-t', '--test', type=str, choices=valid_games, help="Specify the test to run.")
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_arguments()
  shellstation = ShellStation()
  if args.game:
    shellstation.start(game_name=args.game)
  elif args.test:
    run_test(args.test)
  else:
    shellstation.start()
