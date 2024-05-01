from dataclasses import dataclass

@dataclass
class ShellStation:
  games = [1,2,3]

  @classmethod
  def display_logo(self):
    with open("logo.txt", "r") as file:
      logo = file.read()
    print(logo)
  
  @classmethod
  def start(self):
    self.display_logo()
    print('Welcome to ShellStation!')
    print('Select the game you wanna play:')
    print(
      """
        1 - Tic-tac-toe
        2 - Checkers
        3 - Chess
      """
    )
    invalid_choice = True
    while True:
      choice = int(input("Option: "))
      invalid_choice = choice > len(self.games) or choice <= 0
      if invalid_choice:
        print("Invalid choice. Try again.")
      else: 
        print(f'Option {choice} selected.')
        break

if __name__ == "__main__":
  instance = ShellStation()
  instance.start()