import csv
import os
import random
import re

# Constants
GRID_WIDTH = 10  # Number of columns
GRID_HEIGHT = 20  # Number of rows

# Colors
COLORS = {"R", "B", "G", "Y", "M", "C", "W"}  # Red, Blue, Green, Yellow, Magenta, Cyan, White
SHAPES = ["S", "C"]  # Shapes: Square or Circle
TEST_CASES_FOLDER = "Test Cases CSVs"  # Output folder for CSV files
FILENAME_PATTERN = r"^(\d{2}) .*\.csv$"  # Regex to extract first two digits of the filename


def generate_random_board():
    """Generates a board where every cell starts with a random color and as a circle."""
    board = [
        [f"{random.choice(list(COLORS))}C00-00" for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]
    return board


def set_empty_cells(board, empty_percentage):
    """
    Randomly selects cells to set to empty until the specified percentage is reached.
    """
    total_cells = GRID_WIDTH * GRID_HEIGHT
    empty_cells_needed = int(total_cells * empty_percentage)

    # Flatten the board into a list of cell positions
    all_positions = [(row, col) for row in range(GRID_HEIGHT) for col in range(GRID_WIDTH)]
    random.shuffle(all_positions)  # Shuffle to randomize

    # Set cells to empty
    for row, col in all_positions[:empty_cells_needed]:
        board[row][col] = "0000-00"  # Empty cell


def set_square_cells(board, square_percentage):
    """
    Randomly selects non-empty cells to set to squares until the specified percentage is reached.
    """
    total_cells = GRID_WIDTH * GRID_HEIGHT
    square_cells_needed = int(total_cells * square_percentage)

    # Flatten the board into a list of cell positions
    all_positions = [(row, col) for row in range(GRID_HEIGHT) for col in range(GRID_WIDTH)]
    random.shuffle(all_positions)  # Shuffle to randomize

    # Set cells to squares, but skip empty cells
    square_count = 0
    for row, col in all_positions:
        if board[row][col] != "0000-00" and board[row][col][1] == "C":  # Only change circles to squares
            board[row][col] = board[row][col].replace("C", "S", 1)  # Change the shape to square
            square_count += 1
            if square_count >= square_cells_needed:
                break


def get_lowest_unused_file_number(folder):
    """
    Finds the lowest unused numerical value for files in the specified folder using regex.
    """
    try:
        # Ensure the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        filenames = os.listdir(folder)
        used_numbers = set()

        for filename in filenames:
            match = re.match(FILENAME_PATTERN, filename)
            if match:
                used_numbers.add(int(match.group(1)))

        # Find the lowest unused number
        lowest_unused = 1
        while lowest_unused in used_numbers:
            lowest_unused += 1

        return lowest_unused
    except Exception as e:
        print(f"Error finding lowest unused file number: {e}")
        return 1


def save_board_to_csv(board, filename):
    """Saves the board to a single CSV file without a header or trailing newline."""
    filepath = os.path.join(TEST_CASES_FOLDER, filename)
    with open(filepath, "w", newline="") as file:
        writer = csv.writer(file)
        for row in board:
            writer.writerow(row)  # Write each row of the board
    print(f"Board saved as: {filepath}")


if __name__ == "__main__":
    try:
        # Step 1: Generate the initial random board
        board = generate_random_board()
        print("Initial board generated with all cells as random colors and circles.")

        # Step 2: Prompt for the percentage of empty cells
        empty_percentage = float(input("Enter the percentage of empty cells (0–100): ")) / 100.0
        if empty_percentage < 0 or empty_percentage > 1:
            raise ValueError("Invalid percentage. Please enter a value between 0 and 100.")
        set_empty_cells(board, empty_percentage)
        print(f"{empty_percentage * 100}% of cells set to empty.")

        # Step 3: Prompt for the percentage of square cells
        square_percentage = float(input("Enter the percentage of square cells (0–100): ")) / 100.0
        if square_percentage < 0 or square_percentage > 1:
            raise ValueError("Invalid percentage. Please enter a value between 0 and 100.")
        set_square_cells(board, square_percentage)
        print(f"{square_percentage * 100}% of cells set to squares.")

        # Step 4: Get the lowest unused numerical value of existing files
        next_file_number = get_lowest_unused_file_number(TEST_CASES_FOLDER)

        # Step 5: Format the filename
        filename = f"{next_file_number:02} random {int(empty_percentage * 100)} percent empty {int(square_percentage * 100)} percent squares.csv"

        # Step 6: Save the board to the file
        save_board_to_csv(board, filename)

    except Exception as e:
        print(f"An error occurred: {e}")
