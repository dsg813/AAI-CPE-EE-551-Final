from constants import (SQUARE_REQ, EMPTY_REQ, GRID_WIDTH, GRID_HEIGHT,
                       setWhite, getWhite, setColors, getColors, get_boardStateList, set_boardStateList, boardStateList)
import re
import os

# Terminal color codes
COLOR_CODES = {
    "0": "\033[90m",  # Gray for blank
    "R": "\033[91m",  # Bright Red
    "G": "\033[92m",  # Bright Green
    "Y": "\033[93m",  # Bright Yellow
    "B": "\033[94m",  # Bright Blue
    "M": "\033[95m",  # Bright Magenta
    "C": "\033[96m",  # Bright Cyan
    "W": "\033[97m",  # Bright White
    "RESET": "\033[0m"  # Reset to default
}

def updateCodes(board):

    # Process the board up to contiguous item counting
    board = contiguousID(board)
    # print("Board with contiguous regions identified:")
    # printToTerminal(board)

    board = contiguousCount(board)
    # print("Board with contiguous region sizes:")
    # printToTerminal(board)

    if len(boardStateList) == 0:
        appendBoardList(board)

    board, square_changed = squareChanger(board)
    # if square_changed:
    #     print("Board with squares changed for 5+ contiguous cells (Changes made):")
    # else:
    #     print("Board with squares changed for 5+ contiguous cells (No changes):")
    # printToTerminal(board)

    board, erase_changed, eliminated_blocks = eraseChanger(board)
    # if erase_changed:
    #     print("Board with erased clusters of 8+ contiguous cells (Changes made):")
    # else:
    #     print("Board with erased clusters of 8+ contiguous cells (No changes):")
    # printToTerminal(board)

    return board, erase_changed, square_changed, eliminated_blocks


def updateFrame(board):
    """
    Updates the game state frame by frame, processing the board based on game physics
    """
    Eliminated_Total_Blocks = 0

    # Reset boardStateList
    set_boardStateList([])  # Clear the existing board states

    # Add the initial board state to boardStateList


    try:

        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # board = overwriteBoard()
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY
        # COMMENT THIS LINE OUT. FOR TESTING CSV BOARD STATES ONLY

        # print("Initial board state extracted from the game:")
        # printToTerminal(board)



        board, erase_changed, square_changed, eliminated_blocks = updateCodes(board)



        Eliminated_Total_Blocks += eliminated_blocks

        # Outer loop: Continue while there are changes
        changed = True
        while changed:
            # gravity_changer_counter = 0 # used to check number of iterations if desired (1 of 3)
            gravity_changed = False  # Reset gravity change tracker
            
            
            # Inner loop: Gravity operations (run at least once)
            while True:
                # gravity_changer_counter += 1 # used to check number of iterations if desired (2 of 3)

                # Step 1: Gravity Check
                board = gravityCheck(board)
                # print(f"Board with ^ characters for cells contiguous with the bottom row, cycle {gravity_changer_counter}:") # used to check number of iterations if desired (3 of 3)
                # printToTerminal(board)

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
                board, gravity_changed = gravityChanger(board)


                # if gravity_changed:
                #     print(f"After applying gravity changer, cycle {gravity_changer_counter} (Changes made):")
                # else:
                #     print(f"After applying gravity changer, cycle {gravity_changer_counter} (No changes):")
                # printToTerminal(board)


            # Reset 5th characters to '-'
            for y in range(len(board)):
                for x in range(len(board[0])):
                    cell = board[y][x]
                    board[y][x] = cell[:4] + "-" + cell[5:]

            # print("Final board after all gravity operations:")
            # printToTerminal(board)


            board, erase_changed, square_changed, eliminated_blocks = updateCodes(board)
            Eliminated_Total_Blocks += eliminated_blocks
            # Ensure the gravity loop runs at least once
            changed = gravity_changed or square_changed or erase_changed

        # print("All operations completed. Final board:")
        # printToTerminal(board)


        # Update the game state at the end

        appendBoardList(board)

        return board, Eliminated_Total_Blocks

    except Exception as e:
        print(f"An error occurred: {e}")
        return board, 0

# I want to change this to the string print thing in the class
def printToTerminal(board):
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

def contiguousID(board):
    """
    Processes the board using the vision algorithm for each unique color
    """
    unique_colors = set(cell[0] for row in board for cell in row if cell[:4] != "0000")
    for color in unique_colors:
        board = visionAlgorithm(board, color)
    return board

def visionAlgorithm(board, target_color):
    """
    Labels regions based on contiguous blocks, by color
    """
    rows = len(board)
    cols = len(board[0])

    # Initialize MASK and cluster_label with extra row and column
    MASK = []
    cluster_label = []

    for y in range(rows + 1):
        MASK.append([0] * (cols + 1))
        cluster_label.append([999] * (cols + 1))

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
    cluster_label = clusterLabeler(MASK, cluster_label, rows, cols)

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

def contiguousCount(board):
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


def gravityCheck(board):
    """
    Applies a gravity check to the board:
    - Adds an extra row and column for MASK and cluster_label to handle boundary checks.
    - Assigns cluster labels iteratively until stable.
    - Updates the board with ^ or - based on cluster labels connected to the bottom row.
    """
    rows = len(board)
    cols = len(board[0])

    # Initialize MASK and cluster_label with extra row and column
    MASK = []
    cluster_label = []

    for y in range(rows + 1):
        MASK.append([0] * (cols + 1))
        cluster_label.append([999] * (cols + 1))

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
    cluster_label = clusterLabeler(MASK, cluster_label, rows, cols)


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

def squareChanger(board):
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
                        appendBoardList(board)
                except ValueError:
                    print(f"Invalid cluster size in cell {cell} at ({y}, {x}). Skipping.")
    if has_changes == True:
        setWhite(getWhite()+1)

    return board, has_changes


def eraseChanger(board):
    """
    Clusters with 8 or more items are reset to 0000-00
    """
    has_changes = False
    eliminated_blocks = 0

    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                if cluster_size >= EMPTY_REQ:
                    active_power_up = cell[0]
                    if active_power_up == "R":
                        board = redErase(board)
                    elif active_power_up == "G":
                        board = greenErase(board)
                    elif active_power_up == "B":
                        board = blueErase(board)
                    elif active_power_up == "Y":
                        board = yellowErase(board)
                    elif active_power_up == "M":
                        board = magentaErase(board)
                    elif active_power_up == "C":
                        board = cyanErase(board)
                    elif active_power_up == "W":
                        board = whiteErase(board)
                    has_changes = True
                    eliminated_blocks += 1

    return board, has_changes, eliminated_blocks

def gravityChanger(board):
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
                appendBoardList(board)

    return board, has_changes

def clusterLabeler(MASK, cluster_label, rows, cols):
    """
    Labels clusters
    This code is inefficient for now, but it works. It checks every cell, on every iteration
    So if 2 clusters of the same region are bordering, only the cell from the higher number
    cluster will change into that of the smaller numbered cluster
    This process repeats until no changes are made. An optimization could be made to modify the entire cluster
    if any cell in its cluster was modified, but I haven't gotten around to that yet, because it works "fast enough"
    """
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

    return cluster_label


def redErase(board):
    """
    Erase all blocks in the first red cluster with size 8+.
    Mark adjacent cells (up, down, left, right) with a modified cluster ID (red_erase_expanded_ID),
    and then erase all matching cells.
    """
    # print("Red power-up activated: Erasing blocks bordering red clusters of size 8+.")
    # print("Board state before starting:")
    # printToTerminal(board)

    # Step 1: Search for the first red cluster of size 8+
    red_erase_ID = None
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[0] == 'R' and int(cell[-2:]) >= EMPTY_REQ:  # Cluster size condition
                red_erase_ID = cell  # Save the original cluster ID
                break
        if red_erase_ID:
            break

    if not red_erase_ID:
        print("No red cluster of size 8+ found. No action taken.")
        return board

    # Step 2: Generate the expanded cluster ID
    red_erase_expanded_ID = red_erase_ID[:4] + "^" + red_erase_ID[5:]
    # print(f"Red cluster ID to erase: {red_erase_ID}")
    # print(f"Expanded red cluster ID: {red_erase_expanded_ID}")

    # Step 3: Mark adjacent cells (up, down, left, right) with the expanded ID
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == red_erase_ID:
                # Check below
                if (y + 1 < GRID_HEIGHT and board[y + 1][x] != red_erase_ID
                        and board[y + 1][x][0] != "0" and board[y + 1][x][0] != "W"):
                    board[y + 1][x] = red_erase_expanded_ID
                    appendBoardList(board)
                # Check above
                if (y - 1 >= 0 and board[y - 1][x] != red_erase_ID
                        and board[y - 1][x][0] != "0" and board[y - 1][x][0] != "W"):
                    board[y - 1][x] = red_erase_expanded_ID
                    appendBoardList(board)
                # Check to the right
                if (x + 1 < GRID_WIDTH and board[y][x + 1] != red_erase_ID
                        and board[y][x + 1][0] != "0" and board[y][x + 1][0] != "W"):
                    board[y][x + 1] = red_erase_expanded_ID
                    appendBoardList(board)
                # Check to the left
                if (x - 1 >= 0 and board[y][x - 1] != red_erase_ID
                        and board[y][x - 1][0] != "0" and board[y][x - 1][0] != "W"):
                    board[y][x - 1] = red_erase_expanded_ID
                    appendBoardList(board)

    # Step 4: Print the board state after marking adjacent cells
    # print("Board after marking adjacent cells:")
    # printToTerminal(board)

    # Step 5: Erase all cells matching red_erase_ID or red_erase_expanded_ID
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] in (red_erase_ID, red_erase_expanded_ID):
                board[y][x] = "0000-00"
                appendBoardList(board)

    # Step 6: Print the final board state
    # print("Board after red power-up:")
    # printToTerminal(board)


    # boardStateList = get_boardStateList()
    # for i in range(len(boardStateList)):
    #     print(f"\nBoard State {i}:")
    #     printToTerminal(boardStateList[i])  # Print the board in color

    return board

def greenErase(board):
    """
    Erase the first detected green cluster, then apply supergravity column by column.
    """
    # print("Green power-up activated: Erasing first detected green cluster and applying supergravity.")
    # print("Board before green power-up:")
    # printToTerminal(board)

    # Define rows and cols for reuse
    rows = len(board)
    cols = len(board[0])

    # Step 1: Identify the first green cluster of size 8+
    green_erase_ID = None
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[0] == 'G' and int(cell[-2:]) >= EMPTY_REQ:  # Cluster size condition
                green_erase_ID = cell  # Save the first green cell with size >= 8
                break
        if green_erase_ID:
            break

    # print(f"Green cluster ID to erase: {green_erase_ID}")

    # Step 2: Erase all cells matching green_erase_ID
    for y in range(rows):
        for x in range(cols):
            if board[y][x] == green_erase_ID:
                board[y][x] = "0000-00"
                appendBoardList(board)

    # print("Board after erasing green cluster:")
    # printToTerminal(board)

    # Step 3: Apply supergravity
    for col in range(cols):  # Iterate through each column
        for row in range(rows - 1, 0, -1):  # Start from the bottom row and move upward
            iteration_count = 0  # Initialize iteration counter for this row
            while board[row][col] == "0000-00" and iteration_count < rows:  # Check for empty cell
                iteration_count += 1  # Increment the iteration counter

                # Move all cells above down by one
                for above_row in range(row - 1, -1, -1):  # From row above to the top
                    board[above_row + 1][col] = board[above_row][col]
                    appendBoardList(board)
                board[0][col] = "0000-00"  # Clear the top cell after shifting

                # Recheck the same row (reset if it is now filled)
                if board[row][col] != "0000-00":
                    break

    # print("Board after applying supergravity:")
    # printToTerminal(board)
    #
    # print("Board after green power-up:")
    # printToTerminal(board)


    return board


def blueErase(board):
    """
    Erase all blue cells
    """
    # print("Blue power-up activated: Erasing all blue clusters.")
    # print("Board before blue power-up:")
    # printToTerminal(board)

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x][0] == 'B':  # Blue blocks
                board[y][x] = "0000-00"
                appendBoardList(board)

    # print("Board after blue power-up:")
    # printToTerminal(board)


    return board


def yellowErase(board):
    """
    Erase the first detected yellow cluster of size 8+, then erase all square blocks.
    """
    # print("Yellow power-up activated: Erasing first detected yellow cluster and all square blocks.")
    # print("Board before yellow power-up:")
    # printToTerminal(board)

    # Step 1: Identify the first yellow cluster of size 8+
    cluster_code = None
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[0] == 'Y' and int(cell[-2:]) >= EMPTY_REQ:  # Cluster size condition
                cluster_code = cell[2:4]
                break  # Stop after finding the first cluster

    # Step 2: Erase the yellow cluster
    if cluster_code:
        for y in range(len(board)):
            for x in range(len(board[0])):
                cell = board[y][x]
                if cell[0] == 'Y' and cell[2:4] == cluster_code:  # Match cluster code
                    board[y][x] = "0000-00"
                    appendBoardList(board)


    # print("Board after erasing yellow cluster:")
    # printToTerminal(board)

    # Step 3: Erase all square blocks
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000" and cell[1] == 'S' and cell[0] != 'W':  # Non-empty and square
                board[y][x] = "0000-00"
                appendBoardList(board)

    # print("Board after yellow power-up:")
    # printToTerminal(board)


    return board



def magentaErase(board):
    """
    Change all red and blue cells to magenta, rerun the processBoard algorithm if changes are made,
    and erase the first detected magenta cluster of size 8+.
    """
    # print("Magenta power-up activated: Changing red and blue cells to magenta and processing clusters.")
    # print("Board before magenta power-up:")
    # printToTerminal(board)

    # Step 1: Set the `changed` flag and modify the board
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[0] in ('R', 'B'):  # Red or blue blocks
                board[y][x] = 'M' + cell[1:]  # Change to magenta
                appendBoardList(board)

    # print("Board after changing red and blue cells to magenta:")
    # printToTerminal(board)

    # Step 2: Rerun processBoard logic if changes were made
    board = contiguousID(board)
    # print("Board (M) with contiguous regions identified:")
    # printToTerminal(board)

    board = contiguousCount(board)
    # print("Board (M) with contiguous region sizes:")
    # printToTerminal(board)
    #
    # print("Board after rerunning processBoard logic:")
    # printToTerminal(board)

    # Step 3: Erase the first detected magenta cluster of size 8+
    cluster_code = None
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[0] == 'M' and int(cell[-2:]) >= EMPTY_REQ:  # Cluster size condition
                cluster_code = cell[2:4]
                break  # Stop after finding the first cluster

    if cluster_code:
        for y in range(len(board)):
            for x in range(len(board[0])):
                cell = board[y][x]
                if cell[0] == 'M' and cell[2:4] == cluster_code:  # Match cluster code
                    board[y][x] = "0000-00"
                    appendBoardList(board)

    # print("Board after erasing magenta cluster:")
    # printToTerminal(board)


    return board

def cyanErase(board):
    """
    Erase the first detected cyan cluster of size 8+, then apply supergravity to the right.
    """
    # print("Cyan power-up activated: Erasing first detected cyan cluster and applying supergravity to the right.")
    # print("Board before cyan power-up:")
    # printToTerminal(board)

    # Define rows and cols for reuse
    rows = len(board)
    cols = len(board[0])

    # Step 1: Identify the first cyan cluster of size 8+
    cyan_erase_ID = None
    for y in range(rows):
        for x in range(cols):
            cell = board[y][x]
            if cell[0] == 'C' and int(cell[-2:]) >= EMPTY_REQ:  # Cluster size condition
                cyan_erase_ID = cell  # Save the first cyan cell with size >= 8
                break
        if cyan_erase_ID:
            break

    # Step 2: Erase all cells matching cyan_erase_ID
    for y in range(rows):
        for x in range(cols):
            if board[y][x] == cyan_erase_ID:
                board[y][x] = "0000-00"
                appendBoardList(board)

    # print("Board after erasing cyan cluster:")
    # printToTerminal(board)

    # Step 3: Apply supergravity to the right
    for row in range(rows):  # Iterate through each row
        for col in range(cols - 1, 0, -1):  # Start from the rightmost column and move left
            iteration_count = 0  # Initialize iteration counter for this cell
            while board[row][col] == "0000-00" and iteration_count < cols:  # Check for empty cell
                iteration_count += 1  # Increment the iteration counter

                # Move all cells to the right by one
                for left_col in range(col - 1, -1, -1):  # From the current column to the leftmost column
                    board[row][left_col + 1] = board[row][left_col]
                    appendBoardList(board)
                board[row][0] = "0000-00"  # Clear the leftmost cell after shifting

                # Recheck the same column (reset if it is now filled)
                if board[row][col] != "0000-00":
                    break

    # print("Board after cyan power-up:")
    # printToTerminal(board)


    return board

def whiteErase(board):
    """
    Set all blocks to empty.
    """
    # print("White power-up activated: Clearing the entire board.")
    # print("Board before white power-up:")
    # printToTerminal(board)

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != "0000-00":
                board[y][x] = "0000-00"
                appendBoardList(board)

    # print("Board after white power-up:")
    # printToTerminal(board)

    COLORS = getColors()

    if "G" not in COLORS:
        setColors("G", (0, 255, 0))
    elif "B" not in COLORS:
        setColors("B", (0, 0, 255))
    elif "Y" not in COLORS:
        setColors("Y", (255, 255, 0))
    elif "M" not in COLORS:
        setColors("M", (255, 0, 255))
    elif "C" not in COLORS:
        setColors("C", (0, 255, 255))

    return board

def addWhite():
    setWhite(getWhite() + 1)
    print(f"{getWhite()} white circles coming")
    if getWhite() > 0 and "W" not in getColors():
        setColors("W", (255, 255, 255))

def appendBoardList(board):
    # Add the initial board state to boardStateList
    boardStateList = get_boardStateList()
    boardStateList.append([row[:] for row in board])  # Append the copy to the list
    set_boardStateList(boardStateList)  # Update the state


def overwriteBoard():
    """Overwrite the board state by reading the first valid CSV file and updating colors."""
    # Expand the COLORS dictionary
    setColors("G", (0, 255, 0))
    setColors("B", (0, 0, 255))
    setColors("Y", (255, 255, 0))
    setColors("M", (255, 0, 255))
    setColors("C", (0, 255, 255))

    # Folder containing test cases
    TEST_CASES_FOLDER = "Test Cases CSVs"

    # Filename pattern: starts with a 2-digit number followed by any text, ends in .csv
    FILENAME_PATTERN = r"^\d{2}.*\.csv$"

    # Check if the folder exists
    if not os.path.exists(TEST_CASES_FOLDER):
        print(f"Error: Folder '{TEST_CASES_FOLDER}' does not exist.")
        return None

    # Find the first matching file in the folder
    for filename in os.listdir(TEST_CASES_FOLDER):
        if re.match(FILENAME_PATTERN, filename):
            filepath = os.path.join(TEST_CASES_FOLDER, filename)
            try:
                # Read the board from the file
                with open(filepath, "r") as file:
                    board = [line.strip().split(",") for line in file]
                print(f"Successfully loaded board from {filepath}")
                return board
            except Exception as e:
                print(f"Error reading file '{filepath}': {e}")
                return None

    print(f"No test case files matching pattern '{FILENAME_PATTERN}' found.")
    return None
