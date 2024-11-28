import random
from constants import SHAPES
from constants import COLORS

class Tetrimino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        raw_shape = random.choice(SHAPES)
        self.shape = [
            [
                random.randint(1, len(COLORS) - 1) if cell else 0
                for cell in row
            ]
            for row in raw_shape
        ]

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
