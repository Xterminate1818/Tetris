import numpy as np


class Grid:
    def __init__(self, width, height, init=None):
        self.WIDTH = width
        self.HEIGHT = height
        if init is None:
            self._state = self.shape = np.array([[0] * self.WIDTH] * self.HEIGHT)
        else:
            self._state = init

    def solid(self, x: int, y: int) -> bool:
        try:
            return self._state[y, x] != 0
        except IndexError:
            return False

    def get(self, x: int, y: int) -> int:
        return self._state[y, x]

    def sget(self, x: int, y: int) -> int:
        try:
            return self._state[y, x]
        except IndexError:
            return 0

    def set(self, x: int, y: int, val: int) -> None:
        self._state[y, x] = val

    def sset(self, x: int, y: int, val: int) -> None:
        if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
            return
        try:
            self.set(x, y, val)
        except IndexError:
            pass

    def rotate(self, turns):
        return np.rot90(self._state, turns)

    def _mask(self, mask_type, other, offset_x, offset_y):
        """
        :param mask_type: 0 = and, 1 = or
        """
        assert other.WIDTH <= self.WIDTH
        assert other.HEIGHT <= self.HEIGHT

        for x in range(other.WIDTH):
            for y in range(other.HEIGHT):
                nx = x + offset_x
                ny = y + offset_y
                if mask_type == 0:
                    self.sset(nx, ny, self.sget(nx, ny) if (self.solid(nx, ny) and other.solid(x, y)) else 0)
                elif mask_type == 1:
                    self.sset(nx, ny, self.sget(nx, ny) if (self.solid(nx, ny) and other.solid(x, y)) else 0)

    def and_mask(self, other, offset_x=0, offset_y=0):
        self._mask(0, other, offset_x, offset_y)

    def or_mask(self, other, offset_x=0, offset_y=0):
        self._mask(1, other, offset_x, offset_y)

    def collides(self, other, offset_x=0, offset_y=0) -> bool:
        for x in range(other.WIDTH):
            for y in range(other.HEIGHT):
                nx = x + offset_x
                ny = y + offset_y
                if self.solid(nx, ny) and other.solid(x, y):
                    return True
        return False
