import pygame as pg
import sys
from board import Board


if __name__ == "__main__":
    pg.init()
    b = Board()
    b.new_piece()

    display = pg.display.set_mode((250, 500))
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    b.shift_x(-1)
                if event.key == pg.K_RIGHT:
                    b.shift_x(1)
                if event.key == pg.K_DOWN:
                    b.apply_gravity()

                if event.key == pg.K_z:
                    b.rotate_current(1)
                if event.key == pg.K_x:
                    b.rotate_current(-1)

                if event.key == pg.K_SPACE:
                    b.drop()

        display.fill((0, 0, 0))
        # Draw
        b.draw(display)
        pg.display.flip()
        clock.tick(60)
