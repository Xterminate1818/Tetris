import numpy as np
import pygame as pg
from grid import Grid
from tetromino import random_tetromino


def get_color(x, y) -> tuple[int, int, int]:
    return x * 10 % 256, y * 10 % 256, 255


class Board(Grid):
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGHT)
        self.active = None
        self.size = 25

    def _draw_board(self, dis) -> None:
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if not self.sget(x, y):
                    continue
                rect = (x * self.size, y * self.size, self.size, self.size)
                pg.draw.rect(dis, get_color(x, y), rect)

    def bound_piece(self, piece):
        mask = piece.depth_mask()
        x_min, x_max = 0, 4
        for x in range(4):
            if mask[x] != -1:
                x_min = x
                break
        for x in range(4):
            if mask[x] != -1:
                x_max = x
        if piece.x + x_min < 0:
            piece.x = -x_min
        if piece.x + x_max >= self.WIDTH:
            piece.x = self.WIDTH - (x_max + 1)
        return piece

    def shift_x(self, direction):
        if self.collides(self.active, self.active.x + direction, self.active.y):
            return
        self.active.x += direction
        self.bound_piece(self.active)

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

    def new_piece(self):
        self.active = random_tetromino()
        self.active.x = 0
        self.active.y = 0

    def freeze_active(self) -> None:
        self.or_mask(self.active, self.active.x, self.active.y)
        self.validate()
        self.new_piece()

    def apply_gravity(self) -> bool:
        if self.collides(self.active, self.active.x, self.active.y + 1):
            self.freeze_active()
            return True
        for i in self.active.depth_mask():
            if i != -1 and self.active.y + i >= 20:
                self.freeze_active()
                return True
        self.active.y += 1
        return False

    def rotate_current(self, turns):
        self.active.rotate(turns)
        self.bound_piece(self.active)
        if self.collides(self.active, self.active.x, self.active.y):
            self.active.rotate(-turns)
            self.bound_piece(self.active)

    def drop(self):
        while not self.apply_gravity():
            pass

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
                if self.sget(x, y):
                    empty = False
                else:
                    full = False
                if not empty and not full:
                    break
            if full or empty:
                self._state = np.delete(self._state, y, axis=0)
                self._state = np.insert(self._state, 0, [False] * 10, axis=0)
