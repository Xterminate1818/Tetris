import random
import numpy as np
from grid import Grid

random.seed()


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


class O_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([[False] * 4, [False, True, True, False], [False, True, True, False], [False] * 4, ]))


class I_Block(Tetromino):
    state1 = np.array([[False, False, True, False]] * 4)
    state2 = np.rot90(state1)

    def __init__(self):
        super().__init__(self.state1)
        self.current_state = 1

    def rotate(self, turns):
        if turns % 2 == 0:
            return
        if self.current_state == 1:
            self.current_state = 2
            self._state = self.state2
            return
        if self.current_state == 2:
            self.current_state = 1
            self._state = self.state1


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


class S_Block(Tetromino):
    def __init__(self):
        super().__init__(np.array([
            [False]*4,
            [False, True, True, False],
            [False, False, True, True],
            [False]*4
        ]
        ))


class Z_Block(S_Block):
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


running_set = [0, 1, 2, 3, 4, 5, 6]


def random_tetromino() -> Tetromino:
    global running_set
    if len(running_set) == 0:
        running_set = [0, 1, 2, 3, 4, 5, 6]
    r = running_set.pop(random.randrange(len(running_set)))
    print(r)
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
