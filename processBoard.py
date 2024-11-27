import csv

# Terminal color codes
COLOR_CODES = {
    "R": "\033[91m",  # Red
    "G": "\033[92m",  # Green
    "Y": "\033[93m",  # Yellow
    "B": "\033[94m",  # Blue
    "0": "\033[90m",  # Gray for blank
    "RESET": "\033[0m"  # Reset to default
}

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
    next_label = 0
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

                    if larger_label != smaller_label:
                        label_equivalences[larger_label] = smaller_label

    # Resolve equivalences
    resolved_labels = {}
    for label in range(1, next_label):
        current_label = label
        while current_label in label_equivalences:
            current_label = label_equivalences[current_label]
        resolved_labels[label] = current_label

    for y in range(rows):
        for x in range(cols):
            if labels[y][x] != 0:
                labels[y][x] = resolved_labels[labels[y][x]]

    for y in range(rows):
        for x in range(cols):
            if labels[y][x] != 0:
                cluster_id = f"{labels[y][x]:02}"
                board[y][x] = board[y][x][:2] + cluster_id + board[y][x][4:]
    return board

def process_board_with_vision(board):
    """Processes the board using the vision algorithm for each unique color."""
    unique_colors = set(cell[0] for row in board for cell in row if cell[:4] != "0000")
    for color in unique_colors:
        board = apply_vision_algorithm(board, color)
    return board

def count_contiguous_items(board):
    """Counts contiguous items and updates each cell's last 2 indices with the count."""
    unique_clusters = set(cell[0] + cell[2:4] for row in board for cell in row if cell[:4] != "0000")
    cluster_counts = {cluster: 0 for cluster in unique_clusters}
    for row in board:
        for cell in row:
            cluster_code = cell[0] + cell[2:4]
            if cluster_code in cluster_counts:
                cluster_counts[cluster_code] += 1
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            cluster_code = cell[0] + cell[2:4]
            if cluster_code in cluster_counts:
                count = cluster_counts[cluster_code]
                board[y][x] = cell[:5] + f"{count:02}"
    return board
