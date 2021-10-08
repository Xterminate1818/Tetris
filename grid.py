import numpy as np


class Grid:
    def __init__(self, width, height, init=None):
        self.WIDTH = width
        self.HEIGHT = height
        if init is None:
            self._state = self.shape = np.array([[False] * self.WIDTH] * self.HEIGHT)
        else:
            self._state = init

    def get(self, x: int, y: int) -> bool:
        return self._state[y, x]

    def sget(self, x: int, y: int) -> bool:
        try:
            return self._state[y, x]
        except IndexError:
            return False

    def set(self, x: int, y: int, val: bool) -> None:
        self._state[y, x] = val

    def sset(self, x: int, y: int, val: bool) -> None:
        try:
            self.set(x, y, val)
        except IndexError:
            pass

    def rotate(self, turns):
        self._state = np.rot90(self._state, turns)

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
                    self.sset(nx, ny, (self.sget(nx, ny) and other.sget(x, y)))
                elif mask_type == 1:
                    self.sset(nx, ny, (self.sget(nx, ny) or other.sget(x, y)))

    def and_mask(self, other, offset_x=0, offset_y=0):
        self._mask(0, other, offset_x, offset_y)

    def or_mask(self, other, offset_x=0, offset_y=0):
        self._mask(1, other, offset_x, offset_y)

    def collides(self, other, offset_x=0, offset_y=0) -> bool:
        for x in range(other.WIDTH):
            for y in range(other.HEIGHT):
                nx = x + offset_x
                ny = y + offset_y
                if self.sget(nx, ny) and other.sget(x, y):
                    return True
        return False
