import random
from constants import SHAPES, getColors, getWhite, setWhite

class Tetrimino:
    def __init__(self, x, y):  # Default to None
        self.x = x
        self.y = y
        raw_shape = random.choice(SHAPES)
        COLORS = getColors()

        # Initialize shape with explicit loops for better readability
        self.shape = []
        for y in range(len(raw_shape)):
            row = []
            for x in range(len(raw_shape[0])):
                if raw_shape[y][x]:  # If part of the Tetrimino
                    color_index = random.randint(2, len(COLORS) - 1)
                    if getWhite() > 0:
                        color_index = 1
                        setWhite(getWhite()-1)
                    row.append(color_index)
                else:
                    row.append(0)  # Empty cell
            self.shape.append(row)


    def rotate(self):
        # Rotate the Tetrimino shape 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
