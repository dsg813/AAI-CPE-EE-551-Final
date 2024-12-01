from constants import SQUARE_REQ, EMPTY_REQ
# Terminal color codes
COLOR_CODES = {
    "R": "\033[91m",  # Red
    "G": "\033[92m",  # Green
    "Y": "\033[93m",  # Yellow
    "B": "\033[94m",  # Blue
    "0": "\033[90m",  # Gray for blank
    "RESET": "\033[0m"  # Reset to default
}

def update_check(board):
    """
    Updates the game state frame by frame, processing the board based on game physics
    """

    try:
        # Extract the board from the game instance

        print("Initial board state extracted from the game:")
        print_grid_with_colors(board)

        # Process the board up to contiguous item counting
        board = process_board_with_vision(board)
        # print("Board with contiguous regions identified:")
        # print_grid_with_colors(board)

        board = count_contiguous_items(board)
        # print("Board with contiguous region sizes:")
        # print_grid_with_colors(board)

        board, square_changed = square_changer(board)
        # if square_changed:
        #     print("Board with squares changed for 5+ contiguous cells (Changes made):")
        # else:
        #     print("Board with squares changed for 5+ contiguous cells (No changes):")
        # print_grid_with_colors(board)

        board, erase_changed = erase_changer(board)
        # if erase_changed:
        #     print("Board with erased clusters of 8+ contiguous cells (Changes made):")
        # else:
        #     print("Board with erased clusters of 8+ contiguous cells (No changes):")
        # print_grid_with_colors(board)

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
                # print(f"Board with ^ characters for cells contiguous with the bottom row, cycle {gravity_changer_counter}:")
                # print_grid_with_colors(board)

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
                # if gravity_changed:
                #     print(f"After applying gravity changer, cycle {gravity_changer_counter} (Changes made):")
                # else:
                #     print(f"After applying gravity changer, cycle {gravity_changer_counter} (No changes):")
                # print_grid_with_colors(board)

            # Reset 5th characters to '-'
            for y in range(len(board)):
                for x in range(len(board[0])):
                    cell = board[y][x]
                    board[y][x] = cell[:4] + "-" + cell[5:]

            # print("Final board after all gravity operations:")
            # print_grid_with_colors(board)

            # Reprocess the board
            board = process_board_with_vision(board)
            # print("Board with contiguous regions identified:")
            # print_grid_with_colors(board)

            board = count_contiguous_items(board)
            # print("Board with contiguous region sizes:")
            # print_grid_with_colors(board)

            board, square_changed = square_changer(board)
            # if square_changed:
            #     print("Board with squares changed for 5+ contiguous cells (Changes made):")
            # else:
            #     print("Board with squares changed for 5+ contiguous cells (No changes):")
            # print_grid_with_colors(board)

            board, erase_changed = erase_changer(board)
            # if erase_changed:
            #     print("Board with erased clusters of 8+ contiguous cells (Changes made):")
            # else:
            #     print("Board with erased clusters of 8+ contiguous cells (No changes):")
            # print_grid_with_colors(board)

            # Ensure the gravity loop runs at least once
            changed = gravity_changed or square_changed or erase_changed

        print("All operations completed. Final board:")
        print_grid_with_colors(board)


        # Update the game state at the end
        return board

    except Exception as e:
        print(f"An error occurred: {e}")

def print_grid_with_colors(board):
    """
    Prints the grid to the terminal with color-coded cells, disable with comments after testing is done
    """
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
    """
    Processes the board using the vision algorithm for each unique color
    """
    unique_colors = set(cell[0] for row in board for cell in row if cell[:4] != "0000")
    for color in unique_colors:
        board = apply_vision_algorithm(board, color)
    return board

def apply_vision_algorithm(board, target_color):
    """
    Labels regions based on contiguous blocks, by color
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
            # Skip blank cells with color code 0
            if board[y][x][:4] != "0000" and board[y][x][0] == target_color:
                MASK[y + 1][x + 1] = 1  # Offset by 1 for extra row and column

    # Step 2: Set cluster_label = next_label for cells matching the target_color
    for y in range(rows):
        for x in range(cols):
            if MASK[y + 1][x + 1] == 1:  # Process only masked cells
                cluster_label[y + 1][x + 1] = next_label  # Offset by 1 for extra row and column
                next_label += 1

    # Step 3: Assign cluster labels iteratively until stable
    # This code is inefficient for now, but it works. It checks every cell, every iteration
    # So if 2 clusters of the same region are bordering, only the cell from the higher number
    # cluster will change into that of the smaller numbered cluster
    # This process repeats until no changes are made. An optimization could be made to modify the entire cluster
    # if any cell in its cluster was modified, but I haven't gotten around to that yet, because it works "fast enough"
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

    # Step 4: Create a set of all unique cluster labels and map them to cluster IDs
    unique_labels = set()
    for y in range(1, rows + 1):  # Start from 1 to skip the extra boundary row
        for x in range(1, cols + 1):  # Start from 1 to skip the extra boundary column
            label = cluster_label[y][x]
            if label < 999:  # Ignore boundary or unassigned labels
                unique_labels.add(label)

    # Step 4: Update the board with cluster IDs in indices 2 and 3 for the target_color
    # Create a dictionary to map a cluster ID to each cluster label
    label_to_cluster_id = {}
    cluster_id = 1
    for label in sorted(unique_labels):  # Sort to ensure consistent cluster ID mapping
        label_to_cluster_id[label] = f"{cluster_id:02}"
        cluster_id += 1

    for y in range(rows):
        for x in range(cols):
            label = cluster_label[y + 1][x + 1]  # Adjust for the extra row and column
            if label < 999:  # Valid cluster label, 999 is the default for cells outside of the board
                if board[y][x][:4] != "0000":  # Update only non-blank cells
                    # Rebuild the 7-character code with the cluster label
                    board[y][x] = board[y][x][:2] + label_to_cluster_id[label] + board[y][x][4:]

    return board

def count_contiguous_items(board):
    """
    Counts contiguous items and updates each cell's last 2 indices with the count
    """
    rows = len(board)
    cols = len(board[0])

    # Step 1: Create a set of unique cluster codes
    unique_clusters = set()
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cells
                unique_clusters.add(cell[0] + cell[2:4])

    # Step 2: Make a dictionary for cluster counts for each cluster
    cluster_counts = {}
    for cluster in unique_clusters:
        cluster_counts[cluster] = 0  # Initialize count to 0 for each cluster code

    # Step 3: Count occurrences of each cluster code
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cells
                cluster_code = cell[0] + cell[2:4]
                if cluster_code in cluster_counts:
                    if cluster_counts[cluster_code] < 99:
                        cluster_counts[cluster_code] += 1

    # Step 4: Update the board with cluster counts in the last 2 indices
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

    # Step 1: Set MASK = 1 for cells with any color
    for y in range(rows):
        for x in range(cols):
            if board[y][x][:4] != "0000":  # Non-empty cell
                MASK[y + 1][x + 1] = 1  # Offset by 1 for extra row and column

    # Step 2: Set cluster_label = next_label for cells with a color
    for y in range(rows):
        for x in range(cols):
            if board[y][x][:4] != "0000":  # Non-empty cell
                cluster_label[y + 1][x + 1] = next_label  # Offset by 1 for extra row and column
                next_label += 1

    # Step 3: Assign cluster labels iteratively until stable
    # This code is inefficient for now, but it works. It checks every cell, every iteration
    # So if 2 clusters of the same region are bordering, only the cell from the higher number
    # cluster will change into that of the smaller numbered cluster
    # This process repeats until no changes are made. An optimization could be made to modify the entire cluster
    # if any cell in its cluster was modified, but I haven't gotten around to that yet, because it works "fast enough"
    has_changes = True
    while has_changes:
        has_changes = False  # Reset change flag

        # Mask dimensions are over-sized by 1
        for y in range(1, rows + 1):
            for x in range(1, cols + 1):
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


    # Step 4: Find all cluster labels connected to the bottom row
    bottom_row_labels = set(cluster_label[rows][x] for x in range(1, cols + 1))

    # Step 5: Mark cells as ^ or - based on connectivity to the bottom row
    for y in range(rows):
        for x in range(cols):
            if cluster_label[y + 1][x + 1] in bottom_row_labels and board[y][x][:4] != "0000":
                board[y][x] = board[y][x][:4] + "^" + board[y][x][5:]
            else:
                board[y][x] = board[y][x][:4] + "-" + board[y][x][5:]

    return board

def square_changer(board):
    """
    C for circle, S for square. C changes to S for all clustered cells when cluster size 5+
    """
    has_changes = False
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":  # Non-empty cell
                try:
                    cluster_size = int(cell[-2:])  # Extract cluster size
                    if cluster_size >= SQUARE_REQ and cell[1] == "C":  # Check for 'S' and size condition
                        board[y][x] = cell[0] + "S" + cell[2:]  # Change 'S' to 'C'
                        has_changes = True
                except ValueError:
                    print(f"Invalid cluster size in cell {cell} at ({y}, {x}). Skipping.")
    return board, has_changes


def erase_changer(board):
    """
    Clusters with 8 or more items are reset to 0000-00
    """
    has_changes = False
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                if cluster_size >= EMPTY_REQ:
                    board[y][x] = "0000-00"
                    has_changes = True
    return board, has_changes

def gravity_changer(board):
    """
    Moves cells with a "-" as their 5th character down by one row.
    Assumes gravity_check has already been applied (gravity check assigns ^ to any cell contiguous with the bottom)
    By working from the bottom up, there is no way for a "-" cell to overwrite another cell
    """
    rows = len(board)
    cols = len(board[0])
    has_changes = False

    for y in range(rows - 2, -1, -1):  # Start from second-to-last row
        for x in range(cols):
            cell = board[y][x]
            if cell[4] == "-" and cell[:4] != "0000":  # Check if the 5th character is "-" and cell is non-empty

                board[y + 1][x] = cell  # Move the cell down
                board[y][x] = "0000-00"  # Clear the current cell
                has_changes = True

    return board, has_changes