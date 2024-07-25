import pyautogui
import time
import os

path = os.path.dirname(os.path.dirname(__file__))

def open_terminal():
    if os.name == 'nt':
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.typewrite('powershell')
        pyautogui.press('enter')
    elif os.name == 'posix':
        pyautogui.hotkey('ctrl', 'alt', 't')

def init_ships(player: int) -> None:
    global path
    with open(os.path.join(path, f"test/battleship_setup{player}.txt"), 'r') as file:
        for index, line in enumerate(file):
            pyautogui.typewrite(line)
            time.sleep(1)

# Open the first terminal and move it to the left
open_terminal()
time.sleep(2)  # Wait for the terminal to open
pyautogui.hotkey('win', 'left')
time.sleep(1)

# Open the second terminal and move it to the right
open_terminal()
time.sleep(2)  # Wait for the terminal to open
pyautogui.hotkey('win', 'right')
time.sleep(1)

# Switch to the left terminal and execute the commands
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
pyautogui.typewrite(f'cd {path}\n')
time.sleep(1)
pyautogui.typewrite(f'python{"3" if os.name == "posix" else ""} shellstation.py -g battleship\n')
time.sleep(1)
pyautogui.typewrite('localhost 9999\n')
time.sleep(1)

# Switch to the right terminal and execute the commands
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
pyautogui.typewrite(f'cd {path}\n')
time.sleep(1)
pyautogui.typewrite(f'python{"3" if os.name == "posix" else ""} shellstation.py -g battleship\n')
time.sleep(1)
pyautogui.typewrite('localhost 9999\n')
time.sleep(1)

# Setup each player ships
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
init_ships(1)
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
init_ships(2)

# Apply movements to each player (even lines = player1, odd lines = player2)
with open(os.path.join(path, "test/battleship_attacks.txt"), 'r') as file:
    for index, line in enumerate(file):
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.typewrite(line)
        time.sleep(1)
