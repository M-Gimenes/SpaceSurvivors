import pygame as pg
import os
import sys
import subprocess
from locale import getlocale
from languages import *
from path import path



class UI:
    code = getlocale()[0]
    translation = en_US if code == 'en_US' else pt_BR
    @staticmethod
    def init(screen, scale):    
        UI.sfont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 24)
        UI.mfont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 32)
        UI.lfont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 46)
        UI.xlfont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 60)
        UI.titlefont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 120)
        UI.descriptionfont = pg.font.Font(path('Fonts/DigitalDisco-Thin.ttf'), 14)
        UI.arrows = pg.font.Font(None, 24)
        UI.screen = screen
        UI.dimension = screen.get_size()
        UI.center = (screen.get_size()[0]//2, screen.get_size()[1]//2)
        UI.half_width = screen.get_size()[0]//2
        UI.half_height = screen.get_size()[1]//2
        UI.scale = scale
        UI.colors = {'blue':'#003264','light-blue':'#99ccff','black':'#000000','white':'#EBF7FE', 'red':'#780000', 'ice-blue':'#add8e61a'}
        UI.clock = pg.time.Clock()
        UI.FPS = 60

        UI.version = '0.5.1'  #antiga

        UI.fonts = {
            'sm':UI.sfont,
            'm':UI.mfont,
            'l':UI.lfont,
            'xl':UI.xlfont,
            'title':UI.titlefont,
            'description':UI.descriptionfont,
            'arrows': UI.arrows
        }

    def load_language(data):
        if 'language' in data:
            code = data['language']
        else:
            code = getlocale()[0]
        UI.translation = en_US if code == 'en_US' else pt_BR

    def display_text(key):
        return UI.translation.get(key, f'Missing translation: {key}')

    def restart_program():
        python = sys.executable
        script = os.path.abspath(sys.argv[0])
        subprocess.Popen([python, script] + sys.argv[1:])
        sys.exit()