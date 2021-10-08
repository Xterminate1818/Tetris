import pygame as pg
import sys
from tetromino import *
from board import Board


if __name__ == "__main__":
    pg.init()
    b = Board()
    b.active = I_Block()

    display = pg.display.set_mode((250, 500))
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    b.active.x -= 1
                if event.key == pg.K_RIGHT:
                    b.active.x += 1
                if event.key == pg.K_UP:
                    b.active.y -= 1
                if event.key == pg.K_DOWN:
                    b.apply_gravity()

                if event.key == pg.K_z:
                    b.active.rotate(1)
                if event.key == pg.K_x:
                    b.active.rotate(-1)
                if event.key == pg.K_SPACE:
                    b.freeze_active()

        display.fill((0, 0, 0))
        # Draw
        b.draw(display)
        pg.display.flip()
        clock.tick(60)
