import random
from constants import SHAPES

class Tetrimino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, len(SHAPES))

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
