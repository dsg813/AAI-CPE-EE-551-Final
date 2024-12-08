import os
from constants import setColors

CSV_PATH = "Test Cases CSVs/default.csv"  # Hardcoded path to the CSV file

def overwrite_board_with_csv(game):
    """Overwrite the game's board state with the contents of a CSV file."""
    try:
        # Update colors dictionary before overwriting board state
        setColors("G", (0, 255, 0))
        setColors("B", (0, 0, 255))
        setColors("Y", (255, 255, 0))
        setColors("M", (255, 0, 255))
        setColors("C", (0, 255, 255))

        board = load_board_from_file(CSV_PATH)
        game.setBoard(board)
        print(f"Successfully loaded board from {CSV_PATH}")
    except Exception as e:
        print(f"Error loading board from {CSV_PATH}: {e}")

def load_board_from_file(filepath):
    """Load a board state from a CSV file."""
    with open(filepath, "r") as file:
        return [line.strip().split(",") for line in file]
