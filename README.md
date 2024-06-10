# ShellStation

ShellStation is a command-line game suite. It allows users to select and play games through an interactive menu or directly via command-line arguments.

## Features

- **Interactive Game Selection**: Users can choose which game to play through a simple command-line menu.
- **Direct Game Launch**: Users have the option to directly start a game using command-line arguments.
- **Extensible**: Adding new games is as straightforward as updating the `ShellStation` class and adding the game files.

## Prerequisites

Before running ShellStation, ensure you have Python installed on your system. The games are built with Python 3.8 or later.

## Installation

1. Clone the repository:
    ```bash
      git clone https://github.com/kelvinleandro/shellstation
      cd ShellStation
    ```

2. No additional libraries are required to run the basic version of the games as they use standard Python libraries.

## Usage

To start ShellStation in interactive mode:

```bash
  python shellstation.py
```

To directly start a specific game:

```bash
  python shellstation.py -g chess
```

The game will ask you to specify a host and port. For example, you can enter:

```bash
  localhost 9999
```

### Available commands

- `-g`, `--game`: Start with the specified game. Options: chess, draughts, tictactoe, hangman.

## Tests

`test` folder contains simulated matches for each game using `pyautogui`.

To run the automated matches:

1. Ensure you have `pyautogui` installed:

```bash
  pip install pyautogui
```

2. Run the file, e.g.:

```bash
  python test/chess_test.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

