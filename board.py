import numpy as np
import pygame as pg
from grid import Grid


def get_color(x, y) -> tuple[int, int, int]:
    return x * 10 % 256, y * 10 % 256, 255


class Board:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.grid = Grid(self.WIDTH, self.HEIGHT)
        self.active = None
        self.size = 25

    def _draw_board(self, dis) -> None:
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if not self.get_tile(x, y):
                    continue
                rect = (x * self.size, y * self.size, self.size, self.size)
                pg.draw.rect(dis, get_color(x, y), rect)

    def _draw_piece(self, dis) -> None:
        if self.active is None:
            return
        for y in range(4):
            for x in range(4):
                if not self.active.get(x, y):
                    continue
                rect = (
                    (self.active.x + x) * self.size,
                    (self.active.y + y) * self.size,
                    self.size, self.size
                )
                pg.draw.rect(dis, get_color(self.active.x + x, self.active.y + y), rect)

    def get_tile(self, x, y) -> bool:
        try:
            return self.grid.get(x, y)
        except IndexError:
            return False

    def set_tile(self, x: int, y: int, val: bool) -> None:
        if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
            return
        try:
            self.grid.set(x, y, val)
        except IndexError:
            pass

    def freeze_active(self) -> None:
        self.grid.or_mask(self.active, self.active.x, self.active.y)
        self.validate()

    def apply_gravity(self) -> bool:
        self.active.y += 1
        if self.active.collides(self.grid, self.active.x, self.active.y + 1):
            self.freeze_active()
            return True
        for i in self.active.depth_mask():
            if i != -1 and self.active.y + i >= 20:
                self.freeze_active()
                return True
        return False

    def draw(self, dis) -> None:
        self._draw_board(dis)
        self._draw_piece(dis)

    # Bit version would erase rows equal to 0 or 2^11-1
    def validate(self) -> None:
        """
            Erases all rows that are either full or empty
        """
        for y in range(self.HEIGHT):
            full = True
            empty = True
            for x in range(self.WIDTH):
                if self.get_tile(x, y):
                    empty = False
                else:
                    full = False
                if not empty and not full:
                    break
            if full or empty:
                self.grid._state = np.delete(self.grid._state, y, axis=0)
                self.grid._state = np.insert(self.grid._state, 0, [False] * 10, axis=0)
