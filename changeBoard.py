def square_changer(board):
    """Changes the second character of each cell to 'C' if the cluster size > 4."""
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                if cluster_size > 4:
                    board[y][x] = cell[0] + "C" + cell[2:]
    return board

def erase_changer(board):
    """Erases clusters with 8 or more items by setting the cell to '0000-00'."""
    for y in range(len(board)):
        for x in range(len(board[0])):
            cell = board[y][x]
            if cell[:4] != "0000":
                cluster_size = int(cell[-2:])
                if cluster_size >= 8:
                    board[y][x] = "0000-00"
    return board
