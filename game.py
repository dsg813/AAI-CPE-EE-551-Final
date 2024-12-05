import pygame
from tetrimino import Tetrimino
from constants import GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, getColors, getWhite, setWhite
from processBoard import updateFrame  # Import the renamed function


class Game:
    def __init__(self):
        self.grid = [["0"] * GRID_WIDTH for _ in range(GRID_HEIGHT)]  # Initialize with background "0"
        self.shape_grid = [["circle" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)
        self.game_over = False
        self.score = 0

    def checkCollision(self, shape, offset_x, offset_y):
        for y in range(len(shape)):
            row = shape[y]
            for x in range(len(row)):
                cell = row[x]
                if cell:
                    new_x = self.current_mino.x + x + offset_x
                    new_y = self.current_mino.y + y + offset_y
                    if (
                        new_x < 0 or
                        new_x >= GRID_WIDTH or
                        new_y >= GRID_HEIGHT or
                        self.grid[new_y][new_x] != "0"  # Check for non-background cells
                    ):
                        return True
        return False

    def lockMino(self, screen):
        """Locks the current Tetrimino into the grid and processes the board."""
        COLORS = getColors()

        # Lock the current Tetrimino into the grid
        for y in range(len(self.current_mino.shape)):
            row = self.current_mino.shape[y]
            for x in range(len(row)):
                cell = row[x]
                if cell:
                    color_key = list(COLORS.keys())[cell]
                    self.grid[self.current_mino.y + y][self.current_mino.x + x] = color_key
                    self.shape_grid[self.current_mino.y + y][self.current_mino.x + x] = "circle"  # Set shape to circle

        # Process the board with update_check
        board = self.getBoard()  # Extract the current board state
        updated_board = updateFrame(board)  # Process the board
        self.setBoard(updated_board)  # Apply the updated board state

        # Spawn a new Tetrimino
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)

        # Update shape grid to "circle"
        for y in range(len(self.current_mino.shape)):
            for x in range(len(self.current_mino.shape[y])):
                if self.current_mino.shape[y][x]:
                    self.shape_grid[self.current_mino.y + y][self.current_mino.x + x] = "circle"

        # Check for game over condition
        if self.checkCollision(self.current_mino.shape, 0, 0):
            self.game_over = True

    def move(self, dx, dy):
        if not self.checkCollision(self.current_mino.shape, dx, dy):
            self.current_mino.x += dx
            self.current_mino.y += dy

    def rotateMino(self):
        old_shape = self.current_mino.shape[:]
        self.current_mino.rotate()
        if self.checkCollision(self.current_mino.shape, 0, 0):
            self.current_mino.shape = old_shape

    def drop(self, screen):
        if not self.checkCollision(self.current_mino.shape, 0, 1):
            self.current_mino.y += 1
        else:
            self.lockMino(screen)

    def drawGrid(self, screen):
        COLORS = getColors()
        for y in range(len(self.grid)):
            row = self.grid[y]
            for x in range(len(row)):
                color_key = row[x]
                color = COLORS[color_key]  # Use the color dictionary with character keys
                shape = self.shape_grid[y][x]
                if shape == "circle":
                    pygame.draw.circle(
                        screen,
                        color,
                        (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2),
                        int(BLOCK_SIZE * 0.475),
                    )
                elif shape == "square":
                    pygame.draw.rect(
                        screen,
                        color,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )
                pygame.draw.rect(
                    screen,
                    (50, 50, 50),  # Gray color for the grid lines
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )

    def drawMino(self, screen):
        COLORS = getColors()
        for y in range(len(self.current_mino.shape)):
            row = self.current_mino.shape[y]
            for x in range(len(row)):
                cell = row[x]
                if cell:
                    color_key = list(COLORS.keys())[cell]  # Get the corresponding key for this color
                    pygame.draw.circle(
                        screen,
                        COLORS[color_key],
                        (
                            (self.current_mino.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2,
                            (self.current_mino.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2,
                        ),
                        int(BLOCK_SIZE * 0.475)
                    )

    def getBoard(self):
        """Extracts the board state from the current game instance."""
        board = []
        for y in range(len(self.grid)):
            row = []
            for x in range(len(self.grid[0])):
                color = self.grid[y][x]

                if self.shape_grid[y][x]:
                    shape = self.shape_grid[y][x][0].upper()
                else:
                    shape = "0"

                if self.grid[y][x] == "0":
                    row.append(f"0000-00")
                else:
                    row.append(f"{color}{shape}00-00")
            board.append(row)
        return board

    def setBoard(self, board):
        """Updates the game state from a given board representation."""
        for y in range(len(board)):
            for x in range(len(board[0])):
                cell = board[y][x]
                self.grid[y][x] = cell[0]  # Update the grid with the color code
                if cell[1] == "C":
                    self.shape_grid[y][x] = "circle"
                elif cell[1] == "S":
                    self.shape_grid[y][x] = "square"
                else:
                    self.shape_grid[y][x] = None