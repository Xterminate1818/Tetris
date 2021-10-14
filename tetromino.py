import random
import numpy as np
from grid import Grid

random.seed()


class Tetromino(Grid):
    def __init__(self, state=None, size=3):
        super().__init__(size, size, init=state)
        self.x = 0
        self.y = 0

    def depth_mask(self) -> list[int]:
        ret = [-1] * self.WIDTH
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if self.get(x, y) and y + 1 >= ret[x]:
                    ret[x] = y + 1
        return ret

    def rotate(self, turns):
        new = Tetromino(np.rot90(self._state), size=self.WIDTH)
        new.x = self.x
        new.y = self.y
        return new

    # Top of the tetromino
    def top(self):
        ret = self.HEIGHT
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if self.get(x, y) and y < ret:
                    ret = y
        return self.y + ret

    # Bottome of the tetromino
    def bottom(self):
        ret = 0
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if self.get(x, y) and y > ret:
                    ret = y
        return self.y + ret

    # Leftmost bound of the tetromino
    def left(self):
        ret = self.WIDTH
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.get(x, y) and x < ret:
                    ret = x
        return self.x + ret

    # Rightmost bound of the tetromino
    def right(self):
        ret = 0
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.get(x, y) and x > ret:
                    ret = x
        return self.x + ret


class O_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([[False] * 4, [False, True, True, False], [False, True, True, False], [False] * 4, ]),
                         size=4)


class I_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array(
            [[False, False, True, False],
             [False, False, True, False],
             [False, False, True, False],
             [False, False, True, False]]),
            size=4)


class L_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([
            [False, True, False],
            [False, True, False],
            [False, True, True],
        ]
        ))


class J_Block(L_Block):
    def __init__(self):
        super().__init__()
        self._state = np.fliplr(self._state)


class T_Block(Tetromino):
    def __init__(self):
        super().__init__(
            np.array(
                [
                    [False, True, False],
                    [False, True, True],
                    [False, True, False],
                ]
            ))


class S_Block(Tetromino):
    def __init__(self):
        super().__init__(
            np.array([
                [True, True, False],
                [False, True, True],
                [False, False, False]]
            ))


class Z_Block(S_Block):
    def __init__(self):
        super().__init__()
        self._state = np.fliplr(self._state)


running_set = [0, 1, 2, 3, 4, 5, 6]


def random_tetromino() -> Tetromino:
    global running_set
    if len(running_set) == 0:
        running_set = [0, 1, 2, 3, 4, 5, 6]
    r = running_set.pop(random.randrange(len(running_set)))
    if r == 0:
        return O_Block()
    if r == 1:
        return I_Block()
    if r == 2:
        return L_Block()
    if r == 3:
        return J_Block()
    if r == 4:
        return T_Block()
    if r == 5:
        return S_Block()
    if r == 6:
        return Z_Block()
    return Tetromino()
