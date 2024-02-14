import pygame as pg
import pygame_textinput as pgTI
import re
from settings import UI
from transition import Transition
from button import Button
from sounds import Sounds


class Login():
    def __init__(self, gameStateManager, saveManager, request) -> None:
        self.gameStateManager = gameStateManager
        self.saveManager = saveManager
        self.request = request

        self.player_info = {'nickname': '', 'score': 0}

        self.fade = Transition()
        self.transition = False

        self.textManager = pgTI.TextInputManager(validator=lambda input: re.match("^[a-zA-Z0-9]{0,12}$", input))
        self.textinput = pgTI.TextInputVisualizer(manager=self.textManager,
                                                  font_object=UI.fonts['m'], 
                                                  antialias=False, 
                                                  font_color=UI.colors['light-blue'], 
                                                  cursor_color=UI.colors['white'], 
                                                  cursor_blink_interval=500)
        
        buttons_input = [
            Button(UI.display_text('instruction1'), UI.fonts['l'], UI.half_width, UI.half_height-125, 0, 'text'),
            Button(UI.display_text('instruction2'), UI.fonts['sm'], UI.half_width, UI.half_height-90, 0, 'text'),
            Button(UI.display_text('instruction3'), UI.fonts['sm'], UI.half_width, UI.half_height-50, 0, 'text'),
            Button(UI.display_text('confirm'), UI.fonts['l'], UI.half_width,UI.half_height+125, 1,'menu')
        ]

        self.buttons = {'buttons_input': buttons_input}

        self.current_buttons = 'buttons_input'

        self.warning1 = Button(UI.display_text('warning1'), UI.fonts['sm'], UI.half_width, UI.half_height+60, 0, 'text')
        self.warning2 = Button(UI.display_text('warning2'), UI.fonts['sm'], UI.half_width, UI.half_height+60, 0, 'text')
        self.warning = []


    def player_input(self, events):
        self.textinput.update(events)
        self.textrect = self.textinput.surface.get_rect(center=(UI.half_width+5,UI.half_height))
        UI.screen.fill((0, 0, 0, 255))
        UI.screen.blit(self.textinput.surface, self.textrect)

        self.player_info['nickname'] = self.textinput.value

        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons[self.current_buttons]:
                    act = button.collide()
                    if act:
                        if act == 1:
                            self.check_availability()

    def check_availability(self):
        action = self.request.set_data(self.player_info)
        if action == 1:
            self.saveManager.save(self.player_info)
            self.transition = True
        elif action == 2:
            self.warning.clear()
            self.warning.append(self.warning2)
        else:
            self.warning.clear()
            self.warning.append(self.warning1)

    def fades(self):
        if self.fade.draw(self.transition):
            self.transition = False
            self.gameStateManager.set_state('menu')
            
    def run(self, dt, events):
        self.player_input(events)
        for button in self.buttons[self.current_buttons]: button.draw()
        for button in self.warning: button.draw()
        self.fades()
        