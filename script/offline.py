import pygame as pg
import sys
from settings import UI
from button import Button


class Offline():
    def __init__(self) -> None:
        buttons_input = [
            Button(UI.display_text('advice1'),
                   UI.fonts['l'], UI.half_width, UI.half_height-125, 0, 'text'),
            Button(UI.display_text('advice2'),
                   UI.fonts['m'], UI.half_width, UI.half_height-90, 0, 'text'),
            Button(UI.display_text('button_quit'),
                   UI.fonts['l'], UI.half_width, UI.half_height+125, 1, 'menu')
        ]

        self.buttons = {'buttons_input': buttons_input}

        self.current_buttons = 'buttons_input'

    def player_input(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons[self.current_buttons]:
                    act = button.collide()
                    if act:
                        if act == 1:
                            pg.quit()
                            sys.exit()

    def run(self, dt, events):
        UI.screen.fill((0, 0, 0, 255))
        self.player_input(events)
        for button in self.buttons[self.current_buttons]:
            button.draw()
