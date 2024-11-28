def square_changer(board):
    """Changes the second character of each cell to 'C' if the cluster size > 4 and the second character is 'S'."""
    has_changes = False
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                # Only change S to C if cluster size > 4
                if cluster_size > 4 and cell[1] == "S":
                    board[y][x] = cell[0] + "C" + cell[2:]
                    has_changes = True
    return board, has_changes

def erase_changer(board):
    """Erases clusters with 8 or more items by setting the cell to '0000-00'."""
    has_changes = False
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                if cluster_size >= 8:
                    board[y][x] = "0000-00"
                    has_changes = True
    return board, has_changes

def gravity_changer(board):
    """
    Moves cells with a "-" as their 5th character down by one row.
    Assumes gravity_check has already been applied and processes from the bottom row upward.
    Returns True if any changes are made to the board, otherwise False.
    """
    rows = len(board)
    cols = len(board[0])
    has_changes = False  # Track if any changes are made

    # Process each row starting from the second-to-last row upward
    for y in range(rows - 2, -1, -1):  # Start from second-to-last row
        for x in range(cols):
            cell = board[y][x]
            if cell[4] == "-" and cell[:4] != "0000":  # Check if the 5th character is "-"
                # Move current cell down and clear the original position
                board[y + 1][x] = cell  # Move the cell down
                board[y][x] = "0000-00"  # Set current cell to empty
                has_changes = True  # Mark that a change has been made

    return board, has_changes