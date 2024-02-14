import os
import sys
import pygame as pg
import threading
from settings import UI
from button import Button


class Update():
    def __init__(self, gameStateManager, saveManager, request) -> None:
        self.gameStateManager = gameStateManager
        self.saveManager = saveManager
        self.request = request

        buttons_download = [
            Button(UI.display_text('version'), UI.fonts['l'], UI.half_width, UI.half_height-100, 0, 'text'),
            Button(UI.display_text('download'), UI.fonts['l'], UI.half_width,UI.half_height+100, 1,'menu')
        ]

        buttons_waiting1 = [
            Button(UI.display_text('wait1'), UI.fonts['l'], UI.half_width, UI.half_height, 0, 'text'),
        ]
        buttons_waiting2 = [
            Button(UI.display_text('wait2'), UI.fonts['l'], UI.half_width, UI.half_height, 0, 'text'),
        ]
        buttons_waiting3 = [
            Button(UI.display_text('wait3'), UI.fonts['l'], UI.half_width, UI.half_height, 0, 'text'),
        ]


        self.buttons = {'buttons_download': buttons_download,
                        'buttons_waiting1': buttons_waiting1,
                        'buttons_waiting2': buttons_waiting2,
                        'buttons_waiting3': buttons_waiting3}

        self.current_buttons = 'buttons_download'
        self.waiting = False
        self.i = 1

        self.download_thread = threading.Thread(target=self.start_download)

    def player_input(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons[self.current_buttons]:
                    act = button.collide()
                    if act:
                        #self.sound.effect('button', self.sounds_volumes['button'])
                        if act == 1:
                            self.download_thread.start()
                            self.waiting = True

    def start_download(self):
        temp_path = os.path.join(os.getcwd(), "temp_game.exe")
        self.request.download_update(temp_path)
        name_exe = sys.argv[0]
        new_executable_name = "temp_game_old(delete_this).exe"
        os.rename(name_exe, new_executable_name)
        os.replace(temp_path, name_exe)
        os.execl(sys.executable, sys.executable, *sys.argv)

    def wait(self):
        self.current_buttons = f'buttons_waiting{int(self.i)}'
        self.i += 1/30
        if self.i >= 4: self.i = 1

    def run(self, dt, events):
        UI.screen.fill((0, 0, 0, 255))
        self.player_input(events)
        for button in self.buttons[self.current_buttons]: button.draw()
        if self.waiting:
            self.wait()
