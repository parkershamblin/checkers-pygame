# Checkers with Pygame
This repository contains a simple implementation of the classic board game Checkers using Pygame. The game allows two players to play checkers on an 8x8 board, with pieces that can be moved according to the standard rules of checkers.

https://user-images.githubusercontent.com/48718776/58029295-44fedc80-7aea-11e9-958f-cb9cc04e8656.gif

## Features
* Two-player gameplay on an 8x8 board
* Standard and king pieces with appropriate movement and jumping rules
* Basic win condition detection
* Graphical representation of the board and pieces using Pygame
## Requirements
* Python 3.x
* Pygame
## Installation
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/checkers-pygame.git
   ```
2. Navigate to the project directory:
    ```
    cd checkers-pygame
    ```
3. Install the required packages:
    ```
    pip install pygame
    ```

## Usage
Run the main script to start the game:
```
python checkers.py
```

## How to Play
1. The game starts with Player 1 (Red) and Player 2 (Black) pieces placed on the board.
2. Players take turns to move their pieces. A valid move for a pawn is one step diagonally forward to an empty square. A valid move for a king is one step diagonally in any direction to an empty square.
3. Players can jump over an opponent's piece to capture it. Multiple jumps are allowed if the player can continue to jump over opponent's pieces.
4. The game ends when one player captures all the opponent's pieces or when a player has no valid moves left.
