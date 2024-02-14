import pygame as pg
from statistics import mean

pg.init()
aux = pg.display.Info()
SCREENWIDTH, SCREENHEIGHT = aux.current_w, aux.current_h
ratio = 0.6
scale_x = SCREENWIDTH * ratio / 1360
scale_y = SCREENHEIGHT * ratio / 765

screen = pg.display.set_mode(
    (SCREENWIDTH, SCREENHEIGHT), pg.NOFRAME)
scale = mean([scale_x, scale_y])

from game import Game

if __name__ == '__main__':
    start = Game(screen, scale)
    start.run()