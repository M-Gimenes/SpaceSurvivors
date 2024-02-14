import pygame as pg
from settings import UI
from path import path


class Shield():
    shield_animations = {'spawn': [pg.image.load(path(f'Images/shield/spawn/spawn{i}.png')).convert_alpha() for i in range(1, 12+1)],
                         'keep': [pg.image.load(path(f'Images/shield/keep/keep{i}.png')).convert_alpha() for i in range(1, 15+1)],
                         'break': [pg.image.load(path(f'Images/shield/break/break{i}.png')).convert_alpha() for i in range(1, 8+1)]}

    def __init__(self) -> None:
        self.scale = UI.scale * 1.2
        self.dark = pg.surface.Surface
        self.time = {'spawn': 1, 'keep': 1, 'break': 1}
        self.type = 'spawn'
        self.index = {'spawn': 0, 'keep': 0, 'break': 0}

    def animation(self, pos):
        image = Shield.shield_animations[self.type][int(
            self.index[self.type])]
        self.image = pg.transform.scale_by(image, self.scale)
        dark = pg.surface.Surface(self.image.get_size(), pg.SRCALPHA)
        dark.fill((255,255,255,100))
        self.image.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
        self.index[self.type] += len(Shield.shield_animations[self.type]) / \
            (max(UI.clock.get_fps(), 1) * self.time[self.type])
        self.rect = self.image.get_rect(center=pos)
        UI.screen.blit(self.image, self.rect)
        if self.index[self.type] >= len(Shield.shield_animations[self.type]):
            self.index[self.type] = 0
            if self.type == 'spawn': self.type = 'keep'
            return self.type == 'break'

    def change(self, type):
        self.type = type
