from processBoard import read_board_from_csv, print_grid_with_colors, process_board_with_vision, count_contiguous_items, gravity_check
from changeBoard import square_changer, erase_changer, gravity_changer
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
                    print("Board with colors applied:")
                    print_grid_with_colors(board)

                    # Process the board up to contiguous item counting
                    board = process_board_with_vision(board)
                    print("Board with contiguous regions identified:")
                    print_grid_with_colors(board)

                    board = count_contiguous_items(board)
                    print("Board with contiguous region sizes:")
                    print_grid_with_colors(board)

                    board, square_changed = square_changer(board)
                    if square_changed:
                        print("Board with squares changed for 5+ contiguous cells (Changes made):")
                    else:
                        print("Board with squares changed for 5+ contiguous cells (No changes):")
                    print_grid_with_colors(board)

                    board, erase_changed = erase_changer(board)
                    if erase_changed:
                        print("Board with erased clusters of 8+ contiguous cells (Changes made):")
                    else:
                        print("Board with erased clusters of 8+ contiguous cells (No changes):")
                    print_grid_with_colors(board)

                    # Outer loop: Continue while there are changes
                    changed = True
                    while changed:
                        gravity_changer_counter = 0
                        gravity_changed = False  # Reset gravity change tracker

                        # Inner loop: Gravity operations (run at least once)
                        while True:
                            gravity_changer_counter += 1

                            # Step 1: Gravity Check
                            board = gravity_check(board)
                            print(f"Board with ^ characters for cells contiguous with the bottom row, cycle {gravity_changer_counter}:")
                            print_grid_with_colors(board)

                            # Step 2: Check if all non-empty cells are marked with ^
                            all_marked = True
                            for y in range(len(board)):
                                for x in range(len(board[0])):
                                    if board[y][x][:4] != "0000" and board[y][x][4] != "^":  # Non-empty and not marked with ^
                                        all_marked = False
                                        break

                            # If all cells are marked, stop the loop
                            if all_marked:
                                break

                            # Step 3: Apply Gravity Changer
                            board, gravity_changed = gravity_changer(board)
                            if gravity_changed:
                                print(f"After applying gravity changer, cycle {gravity_changer_counter} (Changes made):")
                            else:
                                print(f"After applying gravity changer, cycle {gravity_changer_counter} (No changes):")
                            print_grid_with_colors(board)

                        # Reset 5th characters to '-'
                        for y in range(len(board)):
                            for x in range(len(board[0])):
                                cell = board[y][x]
                                board[y][x] = cell[:4] + "-" + cell[5:]

                        print("Final Board after all gravity operations:")
                        print_grid_with_colors(board)

                        # Reprocess the board
                        board = process_board_with_vision(board)
                        print("Board with contiguous regions identified:")
                        print_grid_with_colors(board)

                        board = count_contiguous_items(board)
                        print("Board with contiguous region sizes:")
                        print_grid_with_colors(board)

                        board, square_changed = square_changer(board)
                        if square_changed:
                            print("Board with squares changed for 5+ contiguous cells (Changes made):")
                        else:
                            print("Board with squares changed for 5+ contiguous cells (No changes):")
                        print_grid_with_colors(board)

                        board, erase_changed = erase_changer(board)
                        if erase_changed:
                            print("Board with erased clusters of 8+ contiguous cells (Changes made):")
                        else:
                            print("Board with erased clusters of 8+ contiguous cells (No changes):")
                        print_grid_with_colors(board)

                        # Ensure the gravity loop runs at least once
                        changed = gravity_changed or square_changed or erase_changed

                except Exception as e:
                    print(f"An error occurred while processing '{filename}': {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
