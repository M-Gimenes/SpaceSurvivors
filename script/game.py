import pygame as pg
import sys
import os
from statistics import mean

from settings import UI
from gameStateManager import GameStateManager
from saveManager import SaveManager
from request import Request
from level import Level
from menu import Menu
from login import Login
from update import Update
from offline import Offline



class Game:
    def __init__(self, screen, scale) -> None:
        UI.init(screen, scale)
        self.gameStateManager = GameStateManager('menu')
        self.request = Request(self.gameStateManager)
        self.saveManager = SaveManager(self.request)
        UI.load_language(self.saveManager.load())
        if self.check_version():
            self.gameStateManager.set_state('update')
        elif not self.saveManager.load() and self.request.get_key():
            self.gameStateManager.set_state('login')

        self.menu = Menu(self.gameStateManager, self.saveManager, self.request)
        self.level = Level(self.gameStateManager, self.saveManager, self.request)
        self.login = Login(self.gameStateManager, self.saveManager, self.request)
        self.update = Update(self.gameStateManager, self.saveManager, self.request)
        self.offline = Offline()
    

        self.states = {'menu': self.menu, 
                    'level': self.level, 
                    'login': self.login, 
                    'update': self.update,
                    'offline': self.offline}

    def run(self) -> None:
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F4 and event.mod == pg.KMOD_ALT):
                    pg.quit()
                    sys.exit()
                    
            dt = (UI.FPS/max(UI.clock.get_fps(), 1))

            self.states[self.gameStateManager.get_state()].run(dt, events)

            pg.display.update()
            UI.clock.tick(30)#arrumar aqui
    
    def check_version(self):
        server_version = self.request.get_version()

        if not server_version:
            return False
        if server_version != UI.version:
            return True
        else:
            self.delete_old()
            return False
    
    def delete_old(self):
        old_executable_name = "temp_game_old(delete_this).exe"
        old_executable_path = os.path.join(os.getcwd(), old_executable_name)
        if os.path.exists(old_executable_path):
            try:
                os.remove(old_executable_path)
            except:
                pass