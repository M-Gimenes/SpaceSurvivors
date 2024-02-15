import pygame as pg
from settings import UI
from path import path


class Explosion(pg.sprite.Sprite):
    explosions = [pg.image.load(path(
        f'Images/explosion/Explosion_blue_circle{i}.png')).convert_alpha() for i in range(1, 10+1)]

    def __init__(self, pos, lvl) -> None:
        super().__init__()

        self.enemies_hit = set()

        self.damage = 4 + 3 * lvl
        self.growth = 1 + 0.25 * lvl
        self.duration = 0.75
        self.pos = pos

        self.image = Explosion.explosions[0]
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)

        self.index = 0

    def animation(self) -> None:
        self.image = pg.transform.scale_by(
            Explosion.explosions[int(self.index)], self.growth)
        self.index += len(Explosion.explosions) / \
            (max(UI.clock.get_fps(), 1) * self.duration)
        if self.index >= len(Explosion.explosions):
            self.kill()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.animation()
