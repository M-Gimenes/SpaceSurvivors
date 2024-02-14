import pygame as pg
from settings import UI
from path import path


class Experience(pg.sprite.Sprite):
    frames = [pg.image.load(path(f'Images/xp/pipo-nazoobj03c_192_{i:02d}.png')).convert_alpha() for i in range(1, 30+1)]
    def __init__(self, pos: tuple) -> None:
        super().__init__()

        self.growth = 0.01
        self.scale = UI.scale * self.growth * 0.55

        self.image = pg.transform.scale_by(Experience.frames[0], self.scale)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pg.mask.from_surface(self.image)

        self.index = 0
        self.pos = pos

    def animation(self) -> None:
        self.image = pg.transform.scale_by(Experience.frames[int(self.index)], self.scale)
        self.index += len(Experience.frames) / \
            (max(UI.clock.get_fps(), 1) * 1)
        if self.index >= len(Experience.frames):
            self.index = 0
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        if self.growth <= 1: self.growth += 1/(max(UI.clock.get_fps(), 1) * 3)
        self.scale = UI.scale * self.growth * 0.6
        self.animation()