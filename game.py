import pygame
from tetrimino import Tetrimino
from constants import GRID_WIDTH, GRID_HEIGHT, COLORS, BLOCK_SIZE

class Game:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)
        self.game_over = False
        self.score = 0


    def drawGrid(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(
                    screen,
                    COLORS[self.grid[y][x]],
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
                    pygame.draw.rect(
                        screen,
                        COLORS[self.current_mino.color],
                        (
                            (self.current_mino.x + x) * BLOCK_SIZE,
                            (self.current_mino.y + y) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )
