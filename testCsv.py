import csv
import os
import random
import re

# Constants
GRID_WIDTH = 10  # Number of columns
GRID_HEIGHT = 20  # Number of rows

# Colors (comment out colors if needed)
COLORS = {
    "R",  # Red
    "B",  # Blue
    "G",  # Green
    "Y"   # Yellow
}

SHAPES = ["S", "C"]  # Shapes: Square or Circle
TEST_CASES_FOLDER = "Test Cases CSVs"  # Output folder for CSV files
FILENAME_PATTERN = r"^(\d{2}) .*\.csv$"  # Regex to extract first two digits of the filename


def generate_random_board(blank_percentage=0):
    """Generates a random board with optional blank cells."""
    board = [
        [
            "0000-00" if random.random() < blank_percentage else f"{random.choice(list(COLORS))}{random.choice(SHAPES)}00-00"
            for _ in range(GRID_WIDTH)
        ]
        for _ in range(GRID_HEIGHT)
    ]
    return board


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
        # Prompt the user for the percentage of empty cells
        blank_percentage = float(input("Enter the percentage of empty cells (0–100): ")) / 100.0
        if blank_percentage < 0 or blank_percentage > 1:
            raise ValueError("Invalid percentage. Please enter a value between 0 and 100.")

        # Generate the random board
        board = generate_random_board(blank_percentage)

        # Get the lowest unused numerical value of existing files
        next_file_number = get_lowest_unused_file_number(TEST_CASES_FOLDER)

        # Format the filename
        filename = f"{next_file_number:02} random {int(blank_percentage * 100)} percent empty.csv"

        # Save the board to the file
        save_board_to_csv(board, filename)

    except Exception as e:
        print(f"An error occurred: {e}")
