# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
COLORS = [
    (0, 0, 0),  # Background
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    #(255, 165, 0),  # Orange
    #(128, 0, 128),  # Purple
    #(0, 255, 255),  # Cyan
]

# Tetrimino Shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1], [1, 1]],        # O shape
    [[1, 1, 1, 1]],          # I shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]]   # J shape
]
