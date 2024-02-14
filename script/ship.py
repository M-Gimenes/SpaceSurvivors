import pygame as pg
from settings import UI
from button import Button
from path import path


class Ship(pg.sprite.Sprite):
    ships = {'1': [pg.image.load(path(f'Fighter/attack1/attack1.{i}.png')).convert_alpha() for i in range(1, 4+1)],
            '2': [pg.image.load(path(f'Fighter/attack2/attack2.{i}.png')).convert_alpha() for i in range(1, 2+1)]}
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x, self.y = x, y
        
        self.image_initial = Ship.ships['1'][0]
        self.rect = self.image_initial.get_rect(center=(self.x,self.y))
        
        self.available = {'1': True, '2': False}
        self.current = '1'
        self.index = 0

        self.text = Button(UI.display_text('lock_ship_2'), UI.fonts['sm'], x, y+50, 0, 'text')
        
    def nextShip(self) -> None:
        self.current = '1' if self.current == '2' else '2'
        self.index = 0

    def animation(self) -> None:
        self.image = Ship.ships[self.current][int(self.index)]
        self.index += len(Ship.ships[self.current]) / \
            (max(UI.clock.get_fps(), 1) * 0.5)
        if self.index >= len(Ship.ships[self.current]):
            self.index = 0
        self.rect = self.image.get_rect(center=(self.x,self.y))

    def block(self):
        if not self.available[self.current]:
            self.mask = pg.mask.from_surface(self.image)
            self.black = self.image.copy()
            if len(self.mask.outline()) > 2:
                pg.draw.polygon(self.black, (0, 0, 0, 225), self.mask.outline(), 0)
                pg.draw.polygon(self.black, UI.colors['white'], self.mask.outline(), 1)
            UI.screen.blit(self.black, (self.rect.topleft))
            self.text.draw()

    def unlock_ship(self, player_info):
        if player_info['score'] >= 180:
            self.available['2'] = True

    def check_ship(self):
        return self.available[self.current]

    def update(self) -> None:
        self.animation()