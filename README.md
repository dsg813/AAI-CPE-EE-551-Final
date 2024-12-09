# Enhanced Tetris Game (Pygame)

A dynamic and enriched take on the traditional Tetris game, this project introduces gameplay mechanics, board analysis, and unique power-up features, all implemented using Python and Pygame.

## Features

- **Classic Tetris Gameplay**: Play with familiar controls for moving, rotating, and dropping Tetriminos.
- **Enhanced Mechanics**:
  - Dynamic scoring based on advanced board state analysis.
  - Special block interactions and cluster-based actions.
- **Power-ups**:
  - Unique power-up effects based on cluster sizes, introducing strategic depth.
- **Interactive Display**: Visual tracking of game state and key events.
- **Custom Game Logic**: Sophisticated mechanics like contiguous block detection, gravity application, and cluster management.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code](#code)
- [Power-ups and Scoring](#power-ups-and-scoring)
- [Controls](#controls)
- [License](#license)

## Requirements

- Python 3.7 or newer
- Pygame library

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/hogan-tech/AAI-CPE-EE-551-Final
   cd AAI-CPE-EE-551-Final
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
tetris-advanced/
├── main.py             # Entry point to run the game
├── game.py             # Core game logic and state management
├── tetrimino.py        # Tetrimino definitions and movement logic
├── constants.py        # Game constants and shared configurations
├── processBoard.py     # Advanced board analysis and mechanics
├── README.md           # Project documentation
└── Test Cases CSVs/    # Test cases for board states (optional)
```

### Summary of Files
- **`main.py`**: The entry point for running the game.
- **`game.py`**: Manages the game state, grid, and interactions.
- **`tetrimino.py`**: Handles the Tetrimino shapes, colors, and rotations.
- **`constants.py`**: Stores constants like grid size, colors, and shapes.
- **`processBoard.py`**: Implements algorithms for block interactions, gravity, and power-ups.

## Power-ups and Scoring
### Power-ups
- **Red**: Expands then erases clusters and adjacent blocks.
- **Green**: Clears blocks and applies vertical "supergravity."
- **Blue**: Removes all blocks of the same color.
- **Yellow**: Erases a cluster and all square blocks.
- **Magenta**: Converts red and blue blocks to magenta, then erases.
- **Cyan**: Clears clusters and applies horizontal "supergravity."
- **White**: Clears the entire board and advances to the next level.

### Scoring
- **Points** are awarded for clearing clusters, with bonuses for large or strategic actions:
- **Cluster** Clearing: +1 point per cluster block.
- **Advanced** Actions: +2 points for power-up activations.
- **Level Clearing**: Reset score multiplier.

## Controls

- **Left Arrow**: Move Tetrimino left
- **Right Arrow**: Move Tetrimino right
- **Down Arrow**: Soft drop (faster falling)
- **Up Arrow**: Rotate Tetrimino
- **Close Window**: Quit the game

## License

This project is licensed under the MIT License. See the LICENSE file for details.
