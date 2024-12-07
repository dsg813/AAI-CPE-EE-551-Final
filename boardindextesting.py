import os
import re
import csv
import pygame
from constants import get_boardStateList, set_boardStateList

# Folder containing test cases
TEST_CASES_FOLDER = "Test Cases CSVs"

# Filename pattern: starts with a 2-digit number followed by any text, ends in .csv
FILENAME_PATTERN = r"^\d{2}.*\.csv$"

# Terminal color codes
COLOR_CODES = {
    "0": (128, 128, 128),  # Gray for blank
    "R": (255, 0, 0),      # Red
    "G": (0, 255, 0),      # Green
    "Y": (255, 255, 0),    # Yellow
    "B": (0, 0, 255),      # Blue
    "M": (255, 0, 255),    # Magenta
    "C": (0, 255, 255),    # Cyan
    "W": (255, 255, 255)   # White
}

# Grid dimensions
CELL_SIZE = 20
MARGIN = 2


def draw_board(board, screen):
    """Draws the board on the `pygame` screen."""
    screen.fill((0, 0, 0))  # Clear the screen with black
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            color = COLOR_CODES.get(cell[0], (0, 0, 0))  # Default to black if color not found
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x * (CELL_SIZE + MARGIN), y * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
            )
    pygame.display.flip()  # Update the display


def main():
    """Main function to process CSV test files and sequentially display the board."""
    pygame.init()

    # Set up pygame window
    screen_width, screen_height = 500, 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Board Progression Viewer")
    clock = pygame.time.Clock()

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
            # Read the board from the CSV file
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                initial_board = [row for row in reader]  # Create the initial board state

            # Initialize board
            board = initial_board

            # Reset boardStateList
            set_boardStateList([])  # Clear the existing board states

            # Add the initial board state to boardStateList
            boardStateList = get_boardStateList()
            boardStateList.append([row[:] for row in board])  # Append the copy to the list
            set_boardStateList(boardStateList)  # Update the state

            # Sequentially modify the board
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if board[y][x][0] == "R":  # Check if the first character is 'R'
                        board[y][x] = "0000-00"  # Modify the cell
                        boardStateList = get_boardStateList()
                        boardStateList.append([row[:] for row in board])  # Append the new copy to the list
                        set_boardStateList(boardStateList)  # Update the state

            # Display all board states in pygame window
            running = True
            boardStateList = get_boardStateList()
            for i, board_state in enumerate(boardStateList):
                print(f"Displaying Board State {i}")  # Debugging in terminal
                draw_board(board_state, screen)  # Draw the board on the screen

                # Delay for visibility and allow event handling
                start_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - start_time < 500:  # Show each state for 500ms
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            break
                    if not running:
                        break
                if not running:
                    break

        except Exception as e:
            print(f"Error processing file '{filepath}': {e}")

    pygame.quit()


if __name__ == "__main__":
    main()
