# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
SQUARE_REQ = 5
EMPTY_REQ = 8

# Colors as a dictionary with single-character keys
COLORS = {
    "0": (0, 0, 0),          # Background
    "W": (255, 255, 255),    # White
    "R": (255, 0, 0),        # Red
}

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

whites = {
    "whiteEarned": 0
}

def getColors():
    """Getter for COLORS."""
    return COLORS

def setColors(key, value):
    """Setter for COLORS to add or update color mappings."""
    COLORS[key] = value

def getWhite():
    """Getter for whiteEarned."""
    return whites["whiteEarned"]

def setWhite(whiteCount):
    """Setter for whiteEarned to update its value."""
    whites["whiteEarned"] = whiteCount