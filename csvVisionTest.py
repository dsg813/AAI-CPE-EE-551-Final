import csv
import os
import re

# Terminal color codes
COLOR_CODES = {
    "R": "\033[91m",  # Red
    "G": "\033[92m",  # Green
    "Y": "\033[93m",  # Yellow
    "B": "\033[94m",  # Blue
    "0": "\033[90m",  # Gray for blank
    "RESET": "\033[0m"  # Reset to default
}

# Folder containing test cases
TEST_CASES_FOLDER = "Test Cases CSVs"

# Filename pattern: starts with a 2-digit number followed by any text
FILENAME_PATTERN = r"^\d{2}.*\.csv$"

def read_board_from_csv(filepath):
    """Reads the Tetris board from a CSV file."""
    board = []
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            board.append(row)
    return board

def print_grid_with_colors(board):
    """Prints the grid to the terminal with color-coded cells."""
    for row in board:
        line = ""
        for cell in row:
            color = cell[0]  # First character indicates the color (R, G, B, Y, or 0)
            if color in COLOR_CODES:
                line += f"{COLOR_CODES[color]}{cell}{COLOR_CODES['RESET']} "
            else:
                line += f"{COLOR_CODES['0']}{cell}{COLOR_CODES['RESET']} "  # Default for blank
        print(line)
    print()  # Blank line for spacing

def apply_vision_algorithm(board, target_color):
    """Adjusts the cluster IDs based on the vision algorithm for the target color."""
    rows = len(board)
    cols = len(board[0])
    next_label = 1
    labels = [[0] * cols for _ in range(rows)]  # Initialize labels grid
    label_equivalences = {}  # To store relationships between labels

    # First pass: Assign labels
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[0] == target_color:  # Check if the cell matches the target color
                top_label = labels[y - 1][x] if y > 0 else 0
                left_label = labels[y][x - 1] if x > 0 else 0

                if top_label == 0 and left_label == 0:  # Case 1: No neighbors with labels
                    labels[y][x] = next_label
                    next_label += 1
                elif top_label != 0 and left_label == 0:  # Case 2: Only top has a label
                    labels[y][x] = top_label
                elif top_label == 0 and left_label != 0:  # Case 2: Only left has a label
                    labels[y][x] = left_label
                else:  # Case 3: Both top and left have labels
                    smaller_label = min(top_label, left_label)
                    larger_label = max(top_label, left_label)
                    labels[y][x] = smaller_label

                    # Record equivalence between labels
                    if larger_label != smaller_label:  # Avoid self-referencing loops
                        if larger_label not in label_equivalences:
                            label_equivalences[larger_label] = smaller_label
                        else:
                            # Ensure consistent relationships
                            label_equivalences[larger_label] = min(
                                label_equivalences[larger_label], smaller_label
                            )

    # Debugging: Print label equivalences after the first pass
    #print(f"\nLabel equivalences after first pass for color {target_color}: {label_equivalences}")

    # Second pass: Resolve equivalences
    resolved_labels = {}  # Cache for resolved labels
    for label in range(1, next_label):
        current_label = label
        seen_labels = set()  # Track seen labels to avoid infinite loops
        while current_label in label_equivalences:
            if current_label in seen_labels:  # Debugging: Detect cycles
                print(f"Cycle detected while resolving label {current_label} for color {target_color}")
                break
            seen_labels.add(current_label)
            current_label = label_equivalences[current_label]
        resolved_labels[label] = current_label

    # Debugging: Print resolved labels
    #print(f"Resolved labels for color {target_color}: {resolved_labels}")

    # Apply resolved labels to the grid
    for y in range(rows):
        for x in range(cols):
            if labels[y][x] != 0:
                labels[y][x] = resolved_labels[labels[y][x]]

    # Update the board with resolved cluster IDs
    for y in range(rows):
        for x in range(cols):
            if labels[y][x] != 0:
                cluster_id = f"{labels[y][x]:02}"
                board[y][x] = board[y][x][:2] + cluster_id + board[y][x][4:]  # Update indices 2 and 3

    return board

def process_board_with_vision(board):
    """Processes the board using the vision algorithm for each unique color."""
    # Determine unique colors (excluding 0000)
    unique_colors = set(cell[0] for row in board for cell in row if cell[:4] != "0000")

    # Apply the vision algorithm for each color
    for color in unique_colors:
    #    print(f"\nProcessing color: {color}")
        board = apply_vision_algorithm(board, color)


    return board

def count_contiguous_items(board):
    """
    Counts how many items are contiguous in each cluster.
    Updates each cell's last 2 indices with the count.
    """
    # Create a set of all unique cluster codes (first, third, and fourth characters)
    unique_clusters = set(cell[0] + cell[2:4] for row in board for cell in row if cell[:4] != "0000")

    # Count occurrences of each cluster
    cluster_counts = {cluster: 0 for cluster in unique_clusters}
    for row in board:
        for cell in row:
            cluster_code = cell[0] + cell[2:4]  # Extract the relevant cluster code
            if cluster_code in cluster_counts:
                cluster_counts[cluster_code] += 1

    # Update each cell with the cluster count
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            cluster_code = cell[0] + cell[2:4]
            if cluster_code in cluster_counts:
                count = cluster_counts[cluster_code]
                board[y][x] = cell[:5] + f"{count:02}"  # Update last 2 indices with the count
    return board

def square_changer(board):
    """
    Changes the second character (shape) of each cell to 'C' if the cluster size (last 2 characters) is greater than 4.
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":  # Ignore blank cells
                cluster_size = int(cell[-2:])  # Extract the last two characters as cluster size
                if cluster_size > 4:
                    board[y][x] = cell[0] + "C" + cell[2:]  # Change the second character to 'C'
    return board

def erase_changer(board):
    """
    Erases clusters with 8 or more items by setting the cell to '0000-00'.
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":  # Ignore blank cells
                cluster_size = int(cell[-2:])  # Extract the last two characters as cluster size
                if cluster_size > 7:
                    board[y][x] = "0000-00"  # Erase the cell
    return board


if __name__ == "__main__":
    try:
        # Ensure the folder exists
        if not os.path.exists(TEST_CASES_FOLDER):
            raise FileNotFoundError(f"Folder '{TEST_CASES_FOLDER}' not found.")

        # Filter filenames based on the pattern
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
                    board = read_board_from_csv(filepath)
                    print("Original Tetris Board Grid with Colors:")
                    print_grid_with_colors(board)

                    # Process the board with the vision algorithm
                    board = process_board_with_vision(board)
                    print("Board with contiguous regions identified:")
                    print_grid_with_colors(board)

                    # Count and update contiguous items
                    board = count_contiguous_items(board)
                    print("Board with contiguous region sizes:")
                    print_grid_with_colors(board)

                    # Update the shape clusters with 5 or more items
                    board = square_changer(board)
                    print("Board with shape updated to square for 5+ contiguous cells:")
                    print_grid_with_colors(board)

                    # Erase clusters with 8 or more items
                    board = erase_changer(board)
                    print("Board with erased clusters of 8+ contiguous cells:")
                    print_grid_with_colors(board)

                except Exception as e:
                    print(f"An error occurred while processing '{filename}': {e}")

    except Exception as e:
        print(f"An error occurred: {e}")