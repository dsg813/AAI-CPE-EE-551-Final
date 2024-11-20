
# Tetris Game (Pygame)

This is a Tetris game implemented using Python and Pygame. The project adheres to the standard Tetris rules, allowing users to control falling Tetriminos with the keyboard.

## Features

- Fully functional Tetris gameplay.
- Controls for moving, rotating, and dropping Tetriminos.
- Line clearing and scoring.
- Game over detection.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Controls](#controls)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.7 or newer
- Pygame library

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/hogan-tech/AAI-CPE-EE-551-Final
   cd AAI-CPE-EE-551-FINAL
   ```

2. Install the required dependencies:

   ```bash
   pip install pygame
   ```

## Usage

1. Run the game by executing the `main.py` file:

   ```bash
   python main.py
   ```

2. Use the keyboard to play the game (see [Controls](#controls) below).

3. Enjoy playing Tetris!

## File Structure

```
tetris-pygame/
├── main.py         # Main script to run the game
├── game.py         # Game logic and grid management
├── tetrimino.py    # Tetrimino shapes and movement logic
├── constants.py    # Constants and configuration
├── README.md       # Project documentation (this file)
```

### Summary of Files
- **`main.py`**: The entry point for running the game.
- **`game.py`**: Manages the game state, grid, and interactions.
- **`tetrimino.py`**: Handles the Tetrimino shapes, colors, and rotations.
- **`constants.py`**: Stores constants like grid size, colors, and shapes.

## Controls

- **Left Arrow**: Move Tetrimino left
- **Right Arrow**: Move Tetrimino right
- **Down Arrow**: Soft drop (faster falling)
- **Up Arrow**: Rotate Tetrimino
- **Close Window**: Quit the game

## License

This project is licensed under the MIT License. See the LICENSE file for details.
