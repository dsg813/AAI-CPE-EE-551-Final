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

def process_board_with_vision(board):
    """Processes the board using the vision algorithm for each unique color."""
    unique_colors = set(cell[0] for row in board for cell in row if cell[:4] != "0000")
    for color in unique_colors:
        board = apply_vision_algorithm(board, color)
    return board

def apply_vision_algorithm(board, target_color):
    """
    Adjusts the cluster IDs based on the vision algorithm for the target color:
    - Adds an extra row and column for MASK and cluster_label to handle boundary checks.
    - Assigns cluster labels iteratively until stable for the specified color.
    - Updates the board with cluster IDs in indices 2 and 3 for the target color.
    """
    rows = len(board)
    cols = len(board[0])

    # Initialize MASK and cluster_label with extra row and column
    MASK = [[0] * (cols + 1) for _ in range(rows + 1)]  # 1 for target_color cells, 0 otherwise
    cluster_label = [[999] * (cols + 1) for _ in range(rows + 1)]  # Cluster label for each cell
    next_label = 1  # Start labeling clusters from 1

    # Step 1: Set MASK = 1 for cells matching the target_color
    for y in range(rows):
        for x in range(cols):
            if board[y][x][0] == target_color:  # Check if the cell matches the target color
                MASK[y + 1][x + 1] = 1  # Offset by 1 for extra row and column

    # Step 1: Set cluster_label = next_label for cells matching the target_color
    for y in range(rows):
        for x in range(cols):
            if MASK[y + 1][x + 1] == 1:  # Process only masked cells
                cluster_label[y + 1][x + 1] = next_label  # Offset by 1 for extra row and column
                next_label += 1

    # Step 2: Assign cluster labels iteratively until stable
    has_changes = True
    while has_changes:
        has_changes = False  # Reset change flag

        for y in range(1, rows + 1):  # Start from 1 to skip the extra boundary row
            for x in range(1, cols + 1):  # Start from 1 to skip the extra boundary column
                if MASK[y][x] == 1:  # Process only cells with MASK = 1
                    current_label = cluster_label[y][x]
                    top_label = cluster_label[y - 1][x]  # Above cell
                    left_label = cluster_label[y][x - 1]  # Left cell

                    # Determine the smallest label among current, top, and left
                    smallest_label = min(
                        label for label in [current_label, top_label, left_label] if label < 999
                    )

                    # Update labels if the smallest_label is smaller than the current ones
                    if smallest_label < current_label:
                        cluster_label[y][x] = smallest_label
                        has_changes = True
                    if top_label != 999 and smallest_label < top_label:
                        cluster_label[y - 1][x] = smallest_label
                        has_changes = True
                    if left_label != 999 and smallest_label < left_label:
                        cluster_label[y][x - 1] = smallest_label
                        has_changes = True

    # Step 3: Create a set of all unique cluster labels and map them to cluster IDs
    unique_labels = set()
    for y in range(1, rows + 1):  # Start from 1 to skip the extra boundary row
        for x in range(1, cols + 1):  # Start from 1 to skip the extra boundary column
            label = cluster_label[y][x]
            if label < 999:  # Ignore boundary or unassigned labels
                unique_labels.add(label)

    # Create a dictionary to map a cluster ID to each cluster label
    label_to_cluster_id = {}
    cluster_id = 1
    for label in sorted(unique_labels):  # Sort to ensure consistent cluster ID mapping
        label_to_cluster_id[label] = f"{cluster_id:02}"
        cluster_id += 1

    # Step 4: Update the board with cluster IDs in indices 2 and 3 for the target_color
    for y in range(rows):
        for x in range(cols):
            label = cluster_label[y + 1][x + 1]  # Adjust for the extra row and column
            if label < 999:  # Valid cluster label
                board[y][x] = board[y][x][:2] + label_to_cluster_id[label] + board[y][x][4:]  # Update indices 2 and 3

    return board



def count_contiguous_items(board):
    """Counts contiguous items and updates each cell's last 2 indices with the count."""
    rows = len(board)
    cols = len(board[0])

    # Create a set of unique cluster codes
    unique_clusters = set()
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cells
                unique_clusters.add(cell[0] + cell[2:4])

    # Initialize cluster_counts using a for loop
    cluster_counts = {}
    for cluster in unique_clusters:
        cluster_counts[cluster] = 0  # Initialize count to 0 for each cluster code

    # Count occurrences of each cluster code
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cells
                cluster_code = cell[0] + cell[2:4]
                if cluster_code in cluster_counts:
                    cluster_counts[cluster_code] += 1

    # Update the board with cluster counts in the last 2 indices
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cells
                cluster_code = cell[0] + cell[2:4]
                if cluster_code in cluster_counts:
                    count = cluster_counts[cluster_code]
                    board[y][x] = cell[:5] + f"{count:02}"

    return board


def gravity_check(board):
    """
    Applies a gravity check to the board:
    - Adds an extra row and column for MASK and cluster_label to handle boundary checks.
    - Assigns cluster labels iteratively until stable.
    - Updates the board with ^ or - based on cluster labels connected to the bottom row.
    """
    rows = len(board)
    cols = len(board[0])

    # Initialize MASK and cluster_label with extra row and column
    MASK = [[0] * (cols + 1) for _ in range(rows + 1)]  # 1 for colored cells, 0 otherwise
    cluster_label = [[999] * (cols + 1) for _ in range(rows + 1)]  # Cluster label for each cell
    next_label = 1  # Start labeling clusters from 1

    # Step 1: Set MASK = 1 for cells with a color
    for y in range(rows):
        for x in range(cols):
            if board[y][x][:4] != "0000":  # Non-empty cell
                MASK[y + 1][x + 1] = 1  # Offset by 1 for extra row and column

    # Step 1: Set cluster_label = next_label for cells with a color
    for y in range(rows):
        for x in range(cols):
            if board[y][x][:4] != "0000":  # Non-empty cell
                cluster_label[y + 1][x + 1] = next_label  # Offset by 1 for extra row and column
                next_label += 1

    # Step 2 and Step 3: Assign cluster labels iteratively until stable
    has_changes = True
    while has_changes:
        has_changes = False  # Reset change flag

        for y in range(1, rows + 1):  # Start from 1 to skip the extra boundary row
            for x in range(1, cols + 1):  # Start from 1 to skip the extra boundary column
                if MASK[y][x] == 1:  # Process only colored cells
                    current_label = cluster_label[y][x]
                    top_label = cluster_label[y - 1][x]  # Above cell
                    left_label = cluster_label[y][x - 1]  # Left cell

                    # Update the higher of top/current label to the smaller value
                    if top_label != 999 and current_label < top_label:
                        cluster_label[y - 1][x] = current_label
                        has_changes = True
                    elif top_label < current_label:
                        cluster_label[y][x] = top_label
                        has_changes = True

                    # Update the higher of left/current label to the smaller value
                    if left_label != 999 and current_label < left_label:
                        cluster_label[y][x - 1] = current_label
                        has_changes = True
                    elif left_label < current_label:
                        cluster_label[y][x] = left_label
                        has_changes = True


    # Find all cluster labels connected to the bottom row
    bottom_row_labels = set(cluster_label[rows][x] for x in range(1, cols + 1))

    # Mark cells as ^ or - based on connectivity to the bottom row
    for y in range(rows):
        for x in range(cols):
            if cluster_label[y + 1][x + 1] in bottom_row_labels and board[y][x][:4] != "0000":
                board[y][x] = board[y][x][:4] + "^" + board[y][x][5:]
            else:
                board[y][x] = board[y][x][:4] + "-" + board[y][x][5:]

    return board