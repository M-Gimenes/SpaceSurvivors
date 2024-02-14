import pygame as pg
from settings import UI
from path import path

class Clock():
    clock_animations = {'back': [pg.image.load(path(f'Images/clock/back/back{i}.png')).convert_alpha() for i in range(1, 20+1)],
                        'freeze': [pg.image.load(path(f'Images/clock/freeze/freeze{i}.png')).convert_alpha() for i in range(1, 15+1)]}
    def __init__(self, duration) -> None:
        self.scale = UI.scale * 1.6
        self.duration = duration
        self.index = 0
    
    def animation(self, type: str):
        image = Clock.clock_animations[type][int(self.index)]
        self.image = pg.transform.scale_by(image, self.scale)
        self.index += len(Clock.clock_animations[type]) / \
            (max(UI.clock.get_fps(), 1) * self.duration)
        self.rect = self.image.get_rect(center=UI.center)
        UI.screen.blit(self.image, self.rect)
        if self.index >= len(Clock.clock_animations[type]): 
            print(self.index)
            self.index = 0
            return True
        return False
        

