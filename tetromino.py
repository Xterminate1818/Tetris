import numpy as np
from grid import Grid


class Tetromino(Grid):
    SIZE = 4

    def __init__(self, state=None):
        super().__init__(self.SIZE, self.SIZE, init=state)
        self.x = 0
        self.y = 0

    def depth_mask(self) -> list[int]:
        ret = [-1, -1, -1, -1]
        for x in range(4):
            for y in range(4):
                if self.get(x, y) and y + 1 >= ret[x]:
                    ret[x] = y + 1
        return ret


class Test_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([[True, False, False, False], [False] * 4, [False] * 4, [False] * 4, ]))


class O_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([[False] * 4, [False, True, True, False], [False, True, True, False], [False] * 4, ]))


class I_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([[False, False, True, False]] * 4))


class L_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([
            [False, False, False, False],
            [False, True, False, False],
            [False, True, False, False],
            [False, True, True, False],
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
                    [False, True, False, False],
                    [False, True, True, False],
                    [False, True, False, False],
                    [False, False, False, False],
                ]
            ))
