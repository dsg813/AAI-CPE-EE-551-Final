from processBoard import read_board_from_csv, print_grid_with_colors, process_board_with_vision, count_contiguous_items
from changeBoard import square_changer, erase_changer
import os
import re

# Folder containing test cases
TEST_CASES_FOLDER = "Test Cases CSVs"
FILENAME_PATTERN = r"^\d{2}.*\.csv$"

if __name__ == "__main__":
    try:
        # Ensure the folder exists
        if not os.path.exists(TEST_CASES_FOLDER):
            raise FileNotFoundError(f"Folder '{TEST_CASES_FOLDER}' not found.")

        filenames = [
            f for f in os.listdir(TEST_CASES_FOLDER)
            if re.match(FILENAME_PATTERN, f)
        ]

        if not filenames:
            print("No matching files found.")
        else:
            for filename in filenames:
                filepath = os.path.join(TEST_CASES_FOLDER, filename)
                print(f"\nProcessing file: {filename}")
                try:
                    # Read the board
                    board = read_board_from_csv(filepath)
                    print("Original Tetris Board Grid with Colors:")
                    print_grid_with_colors(board)

                    # Process the board up to contiguous item counting
                    board = process_board_with_vision(board)
                    print("Board with contiguous regions identified:")
                    print_grid_with_colors(board)

                    board = count_contiguous_items(board)
                    print("Board with contiguous region sizes:")
                    print_grid_with_colors(board)

                    # Apply final transformations
                    board = square_changer(board)
                    print("Board with squares changed for 5+ contiguous cells:")
                    print_grid_with_colors(board)

                    board = erase_changer(board)
                    print("Board with erased clusters of 8+ contiguous cells:")
                    print_grid_with_colors(board)

                except Exception as e:
                    print(f"An error occurred while processing '{filename}': {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
