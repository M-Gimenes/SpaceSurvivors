import pygame as pg
from settings import UI
from path import path


class Hud(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.scale = UI.scale * 1

        # health bar
        health_bars = {'left': pg.image.load(path('Images/HPBar_Left.png')).convert_alpha(),
                       'right': pg.image.load(path('Images/HPBar_Right.png')).convert_alpha(),
                       'middle': pg.image.load(path('Images/HPBar_Middle.png')).convert_alpha()}

        width_health = health_bars['left'].get_width(
        ) + health_bars['middle'].get_width() + health_bars['right'].get_width()
        height_health = health_bars['left'].get_height()

        union_health = pg.surface.Surface(
            (width_health, height_health), pg.SRCALPHA)
        union_health.blits(blit_sequence=((health_bars['left'], (0, 0)),
                                          (health_bars['middle'],
                                           (health_bars['left'].get_width(), 0)),
                                          (health_bars['right'], (health_bars['left'].get_width()+health_bars['middle'].get_width(), 0))))

        healthBar_surf = pg.transform.scale_by(union_health, (0.4, 0.9))
        healthBar_mask = pg.mask.from_surface(healthBar_surf)
        healthBar_pos = (20, 20)
        healthBar = {'surface': healthBar_surf,
                     'mask': healthBar_mask, 'pos': healthBar_pos}

        # stamina bar
        stamina_bars = {'left': pg.image.load(path('Images/StaminaBar_Left.png')).convert_alpha(),
                        'right': pg.image.load(path('Images/StaminaBar_Right.png')).convert_alpha(),
                        'middle': pg.image.load(path('Images/StaminaBar_Middle.png')).convert_alpha()}

        width_stamina = stamina_bars['left'].get_width(
        ) + stamina_bars['middle'].get_width() + stamina_bars['right'].get_width()
        height_stamina = stamina_bars['left'].get_height()

        union_stamina = pg.surface.Surface(
            (width_stamina, height_stamina), pg.SRCALPHA)
        union_stamina.blits(blit_sequence=((stamina_bars['left'], (0, 0)),
                                           (stamina_bars['middle'],
                                            (stamina_bars['left'].get_width(), 0)),
                                           (stamina_bars['right'], (stamina_bars['left'].get_width()+stamina_bars['middle'].get_width(), 0))))

        staminaBar_surf = pg.transform.scale_by(union_stamina, (0.3, 0.4))
        staminaBar_mask = pg.mask.from_surface(staminaBar_surf)
        staminaBar_pos = (20, 37)
        staminaBar = {'surface': staminaBar_surf,
                      'mask': staminaBar_mask, 'pos': staminaBar_pos}

        # dodge bar
        dodge_bars = {'left': pg.image.load(path('Images/DodgeBar_Left.png')).convert_alpha(),
                      'right': pg.image.load(path('Images/DodgeBar_Right.png')).convert_alpha(),
                      'middle': pg.image.load(path('Images/DodgeBar_Middle.png')).convert_alpha()}

        width_dodge = dodge_bars['left'].get_width(
        ) + dodge_bars['middle'].get_width() + dodge_bars['right'].get_width()
        height_dodge = dodge_bars['left'].get_height()

        union_dodge = pg.surface.Surface(
            (width_dodge, height_dodge), pg.SRCALPHA)
        union_dodge.blits(blit_sequence=((dodge_bars['left'], (0, 0)),
                                         (dodge_bars['middle'],
                                          (dodge_bars['left'].get_width(), 0)),
                                         (dodge_bars['right'], (dodge_bars['left'].get_width()+dodge_bars['middle'].get_width(), 0))))

        dodgeBar_surf = pg.transform.scale_by(union_dodge, (0.2, 0.4))
        dodgeBar_mask = pg.mask.from_surface(dodgeBar_surf)
        dodgeBar_pos = (20, 52)
        dodgeBar = {'surface': dodgeBar_surf,
                    'mask': dodgeBar_mask, 'pos': dodgeBar_pos}

        # xp bar
        xp_bars = {'left': pg.image.load(path('Images/StaminaBar_Left.png')).convert_alpha(),
                   'right': pg.image.load(path('Images/StaminaBar_Right.png')).convert_alpha(),
                   'middle': pg.image.load(path('Images/StaminaBar_Middle.png')).convert_alpha()}

        width_xp = xp_bars['left'].get_width(
        ) + xp_bars['middle'].get_width() + xp_bars['right'].get_width()
        height_xp = xp_bars['left'].get_height()

        union_xp = pg.surface.Surface((width_xp, height_xp), pg.SRCALPHA)
        union_xp.blits(blit_sequence=((xp_bars['left'], (0, 0)),
                                      (xp_bars['middle'],
                                       (xp_bars['left'].get_width(), 0)),
                                      (xp_bars['right'], (xp_bars['left'].get_width()+xp_bars['middle'].get_width(), 0))))

        xpBar_surf = pg.transform.scale(union_xp, (UI.dimension[0], 8))
        xpBar_mask = pg.mask.from_surface(xpBar_surf)
        xpBar_pos = (0, UI.dimension[1]-8)
        xpBar = {'surface': xpBar_surf, 'mask': xpBar_mask, 'pos': xpBar_pos}

        self.bars = {'health': healthBar, 'stamina': staminaBar,
                     'dodge': dodgeBar, 'xp': xpBar}

    def draw(self, infos):
        self.draw_bar(infos['max_health'], infos['health'], bar='health')
        self.draw_bar(infos['max_stamina'], infos['stamina'], bar='stamina')
        self.draw_bar(1, infos['dodge'], bar='dodge')
        self.draw_bar(infos['max_xp'], infos['xp'], bar='xp')

    def draw_bar(self, max, current, bar):
        if current < 0:
            current = 0
        background = pg.surface.Surface(
            (self.bars[bar]['surface'].get_size()), pg.SRCALPHA)
        current = pg.transform.scale_by(
            self.bars[bar]['surface'], (current/max, 1))
        background.blit(current, (0, 0))
        if len(self.bars[bar]['mask'].outline()) > 2:
            pg.draw.polygon(
                background, (UI.colors['white']), self.bars[bar]['mask'].outline(), 2)
        UI.screen.blit(background, self.bars[bar]['pos'])
