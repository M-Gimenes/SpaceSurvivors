import pygame as pg
import sys
from settings import UI
from button import Button
from slider import Slider
from ship import Ship
from transition import Transition
from sounds import Sounds
from rank import Rank
from path import path


class Menu():
    def __init__(self, gameStateManager, saveManager, request) -> None:
        self.gameStateManager = gameStateManager
        self.saveManager = saveManager
        self.request = request

        self.sound = Sounds(['Lines.ogg'])

        background_surf = pg.image.load(
            path('Images/back1.png')).convert_alpha()
        self.background_surf = pg.transform.scale(
            background_surf, UI.dimension)

        self.dark = pg.surface.Surface(
            self.background_surf.get_size(), pg.SRCALPHA)
        self.dark.fill((0, 0, 0, 150))

        self.fade = Transition()
        self.transition = False

        title = [
            Button('Space', UI.fonts['title'], UI.half_width,
                   UI.half_height - 300, 0, 'text'),
            Button('Survivors', UI.fonts['title'],
                   UI.half_width, UI.half_height - 200, 0, 'text'),
            Button(UI.version, UI.fonts['sm'],
                   UI.dimension[0]-35, 20, 0, 'text')
        ]

        buttons_menu = [
            Button(UI.display_text('button_play'),
                   UI.fonts['m'], UI.half_width, UI.half_height-75, 1, 'menu'),
            Button(UI.display_text('button_rank'),
                   UI.fonts['m'], UI.half_width, UI.half_height, 2, 'menu'),
            Button(UI.display_text('button_options'),
                   UI.fonts['m'], UI.half_width, UI.half_height+75, 3, 'menu'),
            Button(UI.display_text('button_credits'),
                   UI.fonts['m'], UI.half_width, UI.half_height+150, 4, 'menu'),
            Button(UI.display_text('button_quit'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 5, 'menu')
        ]

        buttons_play = [
            Button(UI.display_text('weapon'),
                   UI.fonts['m'], UI.half_width, UI.half_height - 75, 0, 'text'),
            Button('<', UI.fonts['m'], UI.half_width -
                   150, UI.half_height, 6, 'button'),
            Button('>', UI.fonts['m'], UI.half_width +
                   150, UI.half_height, 7, 'button'),
            Button(UI.display_text('button_start'),
                   UI.fonts['m'], UI.half_width, UI.half_height+150, 8, 'menu'),
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        buttons_rank = [
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        buttons_options = [
            Button(UI.display_text('button_sound'),
                   UI.fonts['m'], UI.half_width, UI.half_height-75, 13, 'menu'),
            Button(UI.display_text('button_language'),
                   UI.fonts['m'], UI.half_width, UI.half_height, 10, 'menu'),
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        buttons_languages = [
            Button('English', UI.fonts['m'], UI.half_width,
                   UI.half_height-75, 11, 'menu'),
            Button('Português', UI.fonts['m'],
                   UI.half_width, UI.half_height, 12, 'menu'),
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        buttons_sound = [
            Button(UI.display_text('button_musics'),
                   UI.fonts['m'], UI.half_width-125, UI.half_height-75, 0, 'text'),
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        buttons_credits = [
            Button(UI.display_text('credits1'),
                   UI.fonts['m'], UI.half_width, UI.half_height-250, 0, 'text'),
            Button('Matheus Gimenes',
                   UI.fonts['m'], UI.half_width, UI.half_height-200, 0, 'text'),
            Button(UI.display_text('credits2'),
                   UI.fonts['m'], UI.half_width, UI.half_height-100, 0, 'text'),
            Button('BogartVGM - facebook.com/BogartVGM',
                   UI.fonts['sm'], UI.half_width, UI.half_height-75, 0, 'text'),
            Button('Clearside - clearsidemusic.com',
                   UI.fonts['sm'], UI.half_width, UI.half_height-50, 0, 'text'),
            Button('Neocrey', UI.fonts['sm'],
                   UI.half_width, UI.half_height-25, 0, 'text'),
            Button('PetterTheSturgeon',
                   UI.fonts['sm'], UI.half_width, UI.half_height, 0, 'text'),
            Button('Trevor Lentz',
                   UI.fonts['sm'], UI.half_width, UI.half_height+25, 0, 'text'),
            Button('Zander Noriega',
                   UI.fonts['sm'], UI.half_width, UI.half_height+50, 0, 'text'),
            Button(UI.display_text('credits3'),
                   UI.fonts['m'], UI.half_width, UI.half_height + 100, 0, 'text'),
            Button('Jeti - dafont.com/digital-disco.font',
                   UI.fonts['sm'], UI.half_width, UI.half_height+125, 0, 'text'),
            Button(UI.display_text('button_back'),
                   UI.fonts['m'], UI.half_width, UI.half_height+225, 9, 'menu')
        ]

        self.ship = pg.sprite.GroupSingle(Ship(UI.half_width, UI.half_height))
        self.rank = Rank()
        self.rank_surface = 0

        self.buttons = {'title': title,
                        'buttons_menu': buttons_menu,
                        'buttons_play': buttons_play,
                        'buttons_options': buttons_options,
                        'buttons_rank': buttons_rank,
                        'buttons_credits': buttons_credits,
                        'buttons_languages': buttons_languages,
                        'buttons_sound': buttons_sound}

        self.current_buttons = 'buttons_menu'
        self.pressed = False

        self.sliders = [
            Slider((UI.center[0] + 125, UI.center[1]-75),
                   (200, 30), 0.9, 0, 100, 'music'),
        ]

    def action(self, events) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons[self.current_buttons]:
                    act = button.collide()
                    if act:
                        if act == 1:
                            self.current_buttons = 'buttons_play'
                            self.ship.sprite.unlock_ship(
                                self.saveManager.load())
                        elif act == 2:
                            data = self.saveManager.load()
                            if data:
                                self.request.set_data(data)
                            self.rank_surface = self.rank.render_table(
                                self.request.get_data(), data)
                            self.current_buttons = 'buttons_rank'
                        elif act == 3:
                            self.current_buttons = 'buttons_options'
                        elif act == 4:
                            self.current_buttons = 'buttons_credits'
                        elif act == 5:
                            pg.quit()
                            sys.exit()
                        elif act == 6 or act == 7:
                            self.ship.sprite.nextShip()
                        elif act == 8:
                            if self.ship.sprite.check_ship():
                                self.transition = True
                        elif act == 9:
                            self.current_buttons = 'buttons_menu'
                        elif act == 10:
                            self.current_buttons = 'buttons_languages'
                        elif act == 11:
                            self.saveManager.change('language', 'en_US')
                            UI.restart_program()
                        elif act == 12:
                            self.saveManager.change('language', 'pt_BR')
                            UI.restart_program()
                        elif act == 13:
                            self.current_buttons = 'buttons_sound'

        mouse_pos = pg.mouse.get_pos()
        mouse = pg.mouse.get_pressed()
        if self.current_buttons == 'buttons_sound':
            for slider in self.sliders:
                if slider.container_rect.collidepoint(mouse_pos):
                    if mouse[0]:
                        slider.grabbed = True
                if not mouse[0]:
                    slider.grabbed = False
                if slider.button_rect.collidepoint(mouse_pos):
                    slider.hover()
                if slider.grabbed:
                    slider.move_slider(mouse_pos)
                    slider.hover()
                else:
                    slider.hovered = False
                slider.render()
                slider.display_value()

    def fades(self):
        if self.fade.draw(self.transition):
            self.current_buttons = 'buttons_menu'
            self.transition = False
            self.gameStateManager.set_state('level')
            self.gameStateManager.pass_info(
                weapon=int(self.ship.sprite.current))

    def run(self, dt, events) -> None:
        self.sound.play(self.transition)
        UI.screen.blit(self.background_surf, (0, 0))
        UI.screen.blit(self.dark, (0, 0))
        if self.current_buttons == 'buttons_play':
            self.ship.update()
            self.ship.draw(UI.screen)
            self.ship.sprite.block()
        if self.current_buttons == 'buttons_rank':
            UI.screen.blit(self.rank_surface, (0, 0))
        elif self.current_buttons == 'buttons_credits':
            pass
        else:
            for button in self.buttons['title']:
                button.draw()
        for button in self.buttons[self.current_buttons]:
            button.draw()
        self.action(events)
        self.fades()
