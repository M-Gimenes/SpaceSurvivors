import pygame as pg
from settings import UI
from sounds import Sounds


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int, type: str) -> None:
        self.BUTTONSTATES = {
            True:UI.colors['light-blue'],
            False:UI.colors['white']
        }

        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False
        self.type = type

        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val

        self.container_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pg.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])

        # label
        self.text = UI.fonts['m'].render(str(int(self.get_value())), False, UI.colors['white'], None)
        self.label_rect = self.text.get_rect(center = (self.pos[0], self.slider_top_pos+18))
        
    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self):
        pg.draw.rect(UI.screen, UI.colors['blue'], self.container_rect)
        pg.draw.rect(UI.screen, self.BUTTONSTATES[self.hovered], self.button_rect)
        pg.draw.rect(UI.screen, (UI.colors['white']), self.container_rect, 1)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos
        value = (button_val/val_range)*(self.max-self.min)+self.min
        if self.type == 'music':
            Sounds.set_music_volume(value)

        return value

    def display_value(self):
        if self.hovered:
            self.text = UI.fonts['m'].render(str(int(self.get_value())), False, UI.colors['white'], None)
            UI.screen.blit(self.text, self.label_rect)