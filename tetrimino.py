import random
from constants import SHAPES
from constants import COLORS

class Tetrimino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        raw_shape = random.choice(SHAPES)
        self.shape = []
        
        for row in raw_shape:
            new_row = []
            for cell in row:
                new_row.append(random.randint(1, len(COLORS) - 1) if cell else 0)
            self.shape.append(new_row)


    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
