import os
import re
from processBoard import updateFrame  # Import the update_check function

# Folder containing test cases
TEST_CASES_FOLDER = "Test Cases CSVs"

# Filename pattern: starts with a 2-digit number followed by any text, ends in .csv
FILENAME_PATTERN = r"^\d{2}.*\.csv$"

def main():
    """Main function to test update_check on all valid CSV files."""
    # Check if the folder exists
    if not os.path.exists(TEST_CASES_FOLDER):
        print(f"Error: Folder '{TEST_CASES_FOLDER}' does not exist.")
        return

    # List all matching files in the folder
    test_files = [
        os.path.join(TEST_CASES_FOLDER, filename)
        for filename in os.listdir(TEST_CASES_FOLDER)
        if re.match(FILENAME_PATTERN, filename)
    ]

    if not test_files:
        print(f"No test case files matching pattern '{FILENAME_PATTERN}' found.")
        return

    # Process each test file
    for filepath in test_files:
        try:
            # Read the board from the file
            with open(filepath, "r") as file:
                board = [line.strip().split(",") for line in file]

            # Call update_check
            updateFrame(board)

        except Exception as e:
            print(f"Error processing file '{filepath}': {e}")

if __name__ == "__main__":
    main()
