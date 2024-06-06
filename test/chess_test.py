import pyautogui
import time
import os

def open_powershell():
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.typewrite('powershell')
    pyautogui.press('enter')

path = os.path.dirname(os.path.dirname(__file__))

# Open the first powershell and move it to the left
open_powershell()
time.sleep(2)  # Wait for the powershell to open
pyautogui.hotkey('win', 'left')
# time.sleep(1)

# Open the second powershell and move it to the right
open_powershell()
time.sleep(2)  # Wait for the powershell to open
pyautogui.hotkey('win', 'right')
# time.sleep(1)

# Switch to the left powershell and execute the commands
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
pyautogui.typewrite(f'cd {path}\n')
time.sleep(1)
pyautogui.typewrite('python shellstation.py -g Chess\n')
time.sleep(1)
pyautogui.typewrite('player1 localhost 9999\n')
time.sleep(1)

# Switch to the right powershell and execute the commands
pyautogui.hotkey('alt', 'tab')
time.sleep(1)
pyautogui.typewrite(f'cd {path}\n')
time.sleep(1)
pyautogui.typewrite('python shellstation.py -g Chess\n')
time.sleep(1)
pyautogui.typewrite('player2 localhost 9999\n')
time.sleep(1)

# Apply movements to each player (even lines = player1, odd lines = player2)
with open(os.path.join(path, "test/chess_movements.txt"), 'r') as file:
    for index, line in enumerate(file):
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.typewrite(line)
        time.sleep(2)
