import pygame as pg
from settings import UI


class Transition():
    def __init__(self) -> None:
        self.black = pg.surface.Surface(UI.dimension, pg.SRCALPHA)
        self.fade = 255
        self.time = 1

    def draw(self, activate) -> bool:
        self.black.fill((0,0,0,self.fade))
        UI.screen.blit(self.black, (0,0))
        if activate:
            self.fade += 255/(max(UI.clock.get_fps(), 1) * self.time)
            if self.fade >= 255: self.fade = 255
            return self.fade >= 255
        self.fade -= 255/(max(UI.clock.get_fps(), 1) * self.time)
        if self.fade <= 0: self.fade = 0
        return False
