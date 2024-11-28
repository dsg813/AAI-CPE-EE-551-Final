import pygame

def flash_and_remove(grid, shape_grid, blocks_to_remove, screen, game, flash_count=3, flash_delay=0.2):

    # Change tiles to squares before flashing
    for x, y in blocks_to_remove:
        shape_grid[y][x] = "square"

    # Get the original colors of the blocks
    original_colors = {block: grid[block[1]][block[0]] for block in blocks_to_remove}

    for _ in range(flash_count):
        # Flash: Toggle color to black (off)
        for x, y in blocks_to_remove:
            grid[y][x] = 0  # Set to background color
        game.drawGrid(screen)
        pygame.display.update()
        pygame.time.delay(int(flash_delay * 1000))

        # Flash: Toggle color back to original
        for x, y in blocks_to_remove:
            grid[y][x] = original_colors[(x, y)]  # Restore the original color
        game.drawGrid(screen)
        pygame.display.update()
        pygame.time.delay(int(flash_delay * 1000))

    # Remove blocks permanently
    for x, y in blocks_to_remove:
        grid[y][x] = 0
        shape_grid[y][x] = "circle"

def find_contiguous_blocks(grid, x, y, color, visited):

    rows, cols = len(grid), len(grid[0])
    stack = [(x, y)]
    contiguous_blocks = []

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        contiguous_blocks.append((cx, cy))

        # Check neighbors (no diagonals)
        for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                if grid[ny][nx] == color:
                    stack.append((nx, ny))

    return contiguous_blocks

def popMatches(grid, shape_grid, screen, game, min_size=5, remove_size=8):

    changed = False

    while True:
        rows, cols = len(grid), len(grid[0])
        visited = set()
        blocks_to_remove = []
        blocks_to_square = []

        for y in range(rows):
            for x in range(cols):
                color = grid[y][x]
                if color != 0 and (x, y) not in visited:
                    # Find all contiguous blocks of the same color
                    contiguous_blocks = find_contiguous_blocks(grid, x, y, color, visited)
                    if len(contiguous_blocks) >= remove_size:
                        blocks_to_remove.extend(contiguous_blocks)
                    elif len(contiguous_blocks) >= min_size:
                        blocks_to_square.extend(contiguous_blocks)

        # Mark squares
        for x, y in blocks_to_square:
            shape_grid[y][x] = "square"

        # Flash and remove large regions
        if blocks_to_remove:
            flash_and_remove(grid, shape_grid, blocks_to_remove, screen, game)
            changed = True

        # Apply gravity
        if apply_gravity(grid):
            changed = True
            game.drawGrid(screen)
            pygame.display.update()
            pygame.time.delay(100)  # Delay for visualization

        # Break if no changes are detected
        if not blocks_to_remove and not apply_gravity(grid):
            break

    return changed

def mark_squares(grid, blocks_to_change, shape_grid):

    for x, y in blocks_to_change:
        shape_grid[y][x] = "square"  # Change shape to square

def process_color_matches(grid, min_size=5):

    rows, cols = len(grid), len(grid[0])
    visited = set()
    blocks_to_change = []

    for y in range(rows):
        for x in range(cols):
            color = grid[y][x]
            if color != 0 and (x, y) not in visited:
                # Find all contiguous blocks of the same color
                contiguous_blocks = find_contiguous_blocks(grid, x, y, color, visited)
                if len(contiguous_blocks) >= min_size:
                    blocks_to_change.extend(contiguous_blocks)

    return blocks_to_change

def find_connected_to_bottom(grid):

    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [(x, rows - 1) for x in range(cols) if grid[rows - 1][x] != 0]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))

        # Check neighbors (no diagonals)
        for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1)]:
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 0 and (nx, ny) not in visited:
                stack.append((nx, ny))

    return visited

def apply_gravity(grid):

    rows, cols = len(grid), len(grid[0])
    connected = find_connected_to_bottom(grid)
    moved = False

    # Traverse the grid from bottom to top
    for y in range(rows - 2, -1, -1):  # Start from the second-to-last row
        for x in range(cols):
            if grid[y][x] != 0 and (x, y) not in connected:
                # Move the cell down
                grid[y + 1][x] = grid[y][x]
                grid[y][x] = 0
                moved = True

    return moved

def stabilize_grid(grid, shape_grid, screen, game):

    while apply_gravity(grid):
        game.drawGrid(screen)
        pygame.display.update()
        pygame.time.delay(100)  # Delay for visualization
