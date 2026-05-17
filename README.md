# Checkers with Pygame

A classic two-player Checkers implementation built with Python and Pygame. The game runs on an 8x8 board with standard rules for pawns, kings, jumping, and piece promotion.

![checkers_pygame_gameplay](https://user-images.githubusercontent.com/48718776/58029295-44fedc80-7aea-11e9-958f-cb9cc04e8656.gif)

## Features

- Two-player gameplay on an 8x8 board
- Standard and king pieces with appropriate movement and jumping rules
- Basic win condition detection
- Graphical representation of the board and pieces using Pygame

## Requirements

- Python 3.10-3.12 recommended
- Pygame 2.6.1
- Anaconda (optional, for environment management)

## Installation

1. Clone this repository:
   ```powershell
   git clone https://github.com/yourusername/checkers-pygame.git
   cd checkers-pygame
   ```

2. Set up the environment using Anaconda:
   ```powershell
   conda env create --file environment.yml
   conda activate checkers-pygame-py312
   ```

## Usage

Run the game:

```powershell
python main.py
```

Press **Q** to quit the game at any time.

## How to Play

1. **Starting Position**: Red pieces are at the bottom, Black pieces at the top.
2. **Basic Movement**: Move a pawn one square diagonally forward to an empty square. Kings can move diagonally in any direction.
3. **Capturing**: Jump over an opponent's piece to capture it. Chain multiple jumps in a single turn if possible.
4. **Promotion**: Reach the opposite end of the board with a pawn to promote it to a king.
5. **Winning**: Capture all opponent pieces or leave them with no legal moves to win.
