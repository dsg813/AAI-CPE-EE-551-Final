import pygame
from tetrimino import Tetrimino
from constants import GRID_WIDTH, GRID_HEIGHT, COLORS, BLOCK_SIZE
from colorMatch import popMatches, process_color_matches, mark_squares

class Game:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.shape_grid = [["circle" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)
        self.game_over = False
        self.score = 0

    def checkCollision(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_mino.x + x + offset_x
                    new_y = self.current_mino.y + y + offset_y
                    if (
                        new_x < 0 or 
                        new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        self.grid[new_y][new_x]
                    ):
                        return True
        return False

    def lockMino(self, screen):
        for y, row in enumerate(self.current_mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_mino.y + y][self.current_mino.x + x] = cell

        # Create a shape grid if not already present
        if not hasattr(self, "shape_grid"):
            self.shape_grid = [["circle" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Process color matches and update shapes
        while popMatches(self.grid, self.shape_grid, screen, self):
            pass  # Continue until no more matches or gravity actions are needed

        # Spawn a new Tetrimino
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)
        if self.checkCollision(self.current_mino.shape, 0, 0):
            self.game_over = True

    def move(self, dx, dy):
        if not self.checkCollision(self.current_mino.shape, dx, dy):
            self.current_mino.x += dx
            self.current_mino.y += dy

    def rotate_mino(self):
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
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[self.grid[y][x]]
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
        for y, row in enumerate(self.current_mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.circle(
                        screen,
                        COLORS[cell],
                        (
                            (self.current_mino.x + x) * BLOCK_SIZE + BLOCK_SIZE // 2,
                            (self.current_mino.y + y) * BLOCK_SIZE + BLOCK_SIZE // 2,
                        ),
                        int(BLOCK_SIZE * 0.475)
                    )
