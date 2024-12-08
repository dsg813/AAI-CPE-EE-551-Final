import pygame
from tetrimino import Tetrimino
from constants import COLORS, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, getColors, getMinos, setMinos
from processBoard import updateFrame  # Import the renamed function


class Game:
    def __init__(self):
        self.grid = [["0"] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.shape_grid = [["circle" for _ in range(
            GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)
        self.game_over = False
        self.score = 0
        self.level = 0
        self.whitePoints = 0
        self.font = pygame.font.Font(None, 36)
        self.offset_x = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

    def updateScore(self, newScore):
        self.score += newScore

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
                        self.grid[new_y][new_x] != "0"
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
                    self.grid[self.current_mino.y +
                              y][self.current_mino.x + x] = color_key
                    self.shape_grid[self.current_mino.y +
                                    y][self.current_mino.x + x] = "circle"

        setMinos(getMinos()+1)

        board = self.getBoard()
        updated_board, eliminated_blocks = updateFrame(board)

        self.setBoard(updated_board)

        self.updateScore(eliminated_blocks * 100)

        # Spawn a new Tetrimino

        self.current_mino = Tetrimino(GRID_WIDTH // 2 - 1, 0)

        # Update shape grid to "circle"
        for y in range(len(self.current_mino.shape)):
            for x in range(len(self.current_mino.shape[y])):
                if self.current_mino.shape[y][x]:
                    self.shape_grid[self.current_mino.y +
                                    y][self.current_mino.x + x] = "circle"

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

    def drawGrid(self, screen, offset_x=0):

        for y in range(len(self.grid)):
            row = self.grid[y]
            for x in range(len(row)):
                color_key = row[x]
                color = COLORS[color_key]
                shape = self.shape_grid[y][x]
                rect_x = offset_x + x * BLOCK_SIZE
                rect_y = y * BLOCK_SIZE

                if shape == "circle":
                    pygame.draw.circle(
                        screen,
                        color,
                        (rect_x + BLOCK_SIZE // 2, rect_y + BLOCK_SIZE // 2),
                        int(BLOCK_SIZE * 0.475),
                    )
                elif shape == "square":
                    pygame.draw.rect(
                        screen,
                        color,
                        (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE),
                    )
                pygame.draw.rect(
                    screen,
                    (50, 50, 50),  # Gray color for the grid lines
                    (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )

    def drawMino(self, screen, offset_x=0):
        COLORS = getColors()

        for y in range(len(self.current_mino.shape)):
            row = self.current_mino.shape[y]
            for x in range(len(row)):
                cell = row[x]
                if cell:
                    color_key = list(COLORS.keys())[cell]
                    pygame.draw.circle(
                        screen,
                        COLORS[color_key],
                        (
                            offset_x + (self.current_mino.x + x) *
                            BLOCK_SIZE + BLOCK_SIZE // 2,
                            (self.current_mino.y + y) *
                            BLOCK_SIZE + BLOCK_SIZE // 2,
                        ),
                        int(BLOCK_SIZE * 0.475)
                    )

    def forceSpawnNewMino(self):
        """Forcefully spawns a new Tetrimino and updates the game state."""
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

        # print("Debug: New Tetrimino forcefully spawned")

    # def renderScore(self, screen, offset_x=0, offset_y=0):
    #     score_surface = self.font.render(
    #         f"Score: {self.score}", True, (255, 255, 255))
    #     screen.blit(score_surface, (offset_x, offset_y))
    #
    # def renderLevel(self, screen, offset_x=0, offset_y=0):
    #     level_surface = self.font.render(
    #         f"Level: {self.level}", True, (255, 255, 255))
    #     screen.blit(level_surface, (offset_x, offset_y))
    #
    # def renderWhitePoints(self, screen, offset_x=0, offset_y=0):
    #     white_point_surface = self.font.render(
    #         f"White Points: {self.whitePoints}", True, (255, 255, 255))
    #     screen.blit(white_point_surface, (offset_x, offset_y))
    #
    # def renderRedRule(self, screen, offset_x=0, offset_y=0):
    #     redRule_surface = self.font.render(
    #         f"Rule: XXXXXXX", True, (255, 255, 255))
    #     screen.blit(redRule_surface, (offset_x, offset_y))

    def renderText(self, screen, text, offset_x=0, initial_offset_y=0, line_spacing=30):
        """
        Renders multiple lines of text on the screen.
        """
        lines = text.split("\n")
        y_offset = initial_offset_y
        for line in lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (offset_x, y_offset))
            y_offset += line_spacing

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
                self.grid[y][x] = cell[0]
                if cell[1] == "C":
                    self.shape_grid[y][x] = "circle"
                elif cell[1] == "S":
                    self.shape_grid[y][x] = "square"
                else:
                    self.shape_grid[y][x] = None
