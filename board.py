import numpy as np
from grid import Grid
from tetromino import Tetromino


def get_color(x, y) -> tuple[int, int, int]:
    return x * 10 % 256, y * 10 % 256, 255


class Board(Grid):
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGHT)

    def validate(self) -> None:
        """
            Erases all rows that are either full or empty
        """
        for y in range(self.HEIGHT):
            full = True
            empty = True
            for x in range(self.WIDTH):
                if self.sget(x, y):
                    empty = False
                else:
                    full = False
                if not empty and not full:
                    break
            if full or empty:
                self._state = np.delete(self._state, y, axis=0)
                self._state = np.insert(self._state, 0, [False] * 10, axis=0)

    def height_mask(self, ceil=0):
        ret = [0] * self.WIDTH
        for x in range(self.WIDTH):
            for y in range(ceil, self.HEIGHT):
                if self.get(x, y):
                    ret[x] = self.HEIGHT - y
                    break
        return ret

    def add_piece(self, piece: Tetromino):
        for x in range(piece.WIDTH):
            for y in range(piece.HEIGHT):
                if piece.get(x, y):
                    self.sset(x + piece.x, y + piece.y, True)
        self.validate()

    def bound_piece(self, piece: Tetromino):
        if piece.left() <= 0:
            piece.x = 0
        if piece.right() >= self.WIDTH:
            pass
