import pygame as pg
from math import cos, sin, pi, degrees, atan2
from settings import UI
from path import path


class Projectiles(pg.sprite.Sprite):
    projectiles = {'player1': [pg.image.load(path('Fighter/charge/charge1.1.png')).convert_alpha()],
                    'player2': [pg.image.load(path('Fighter/charge/charge2.1.png')).convert_alpha()],
                    'enemy1': [pg.image.load(path('Bomber/charge/charge1.1.png')).convert_alpha()],
                    'enemy2': [pg.image.load(path(f'Bomber/charge/charge2.{i}.png')).convert_alpha() for i in range(1,4+1)]}
        
    def __init__(self, angle, x, y, sprite, scale, damage, speed) -> None:
        super().__init__()

        self.enemies_hit = set() 

        self.base_damage = damage
        self.damage = self.base_damage
        self.speed = speed 
        self.angle = angle
        self.spin = 2
        
        self.duration = pg.time.get_ticks()

        self.sprite = sprite
        self.scale = scale 
        if self.sprite == 'enemy2':
            self.scale = scale * 2

    
        self.index = 0
       
        self.charge = Projectiles.projectiles[self.sprite][0]
        self.image = pg.transform.rotozoom(self.charge, angle, self.scale)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)

    def dislocation(self, dt, rect_player) -> None:
        if self.sprite == 'enemy2' and (pg.time.get_ticks() - self.duration <= 2500):
            self.fire_angle = -degrees(atan2(
                rect_player[1] - self.rect.centery, rect_player[0] - self.rect.centerx))
            rotate = (self.fire_angle - self.angle + 180) % 360 - 180
            if rotate >= 3:
                self.angle += self.spin * dt
            elif rotate <= -3:
                self.angle -= self.spin * dt
        self.rect.centerx += self.speed * cos((self.angle*pi/180)) * dt
        self.rect.centery -= self.speed * sin((self.angle*pi/180)) * dt

    def change_damage(self, percentage):
        self.damage = self.base_damage * percentage

    def animation(self) -> None:
        if self.sprite == 'enemy2':
            self.charge = Projectiles.projectiles[self.sprite][int(self.index)]
            self.index += len(Projectiles.projectiles[self.sprite]) / \
                (max(UI.clock.get_fps(), 1) * 0.5)
            if self.index >= len(Projectiles.projectiles[self.sprite]):
                self.index = 0
            self.rect = self.charge.get_rect(center=self.rect.center)

    def att_sprite(self) -> None:
        self.image = pg.transform.rotozoom(
            self.charge, self.angle, self.scale)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def destroy(self) -> None:
        if self.rect.top > UI.dimension[1]:
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > UI.dimension[0]:
            self.kill()
        elif self.rect.right < 0:
            self.kill()

    def update(self,dt, rect_player = (0,0)) -> None:
        if len(self.enemies_hit): self.damage
        self.dislocation(dt, rect_player)
        self.animation()
        self.att_sprite()
        self.destroy()
