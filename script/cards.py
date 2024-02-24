import pygame as pg
from random import sample
from settings import UI
from button import Button
from path import path


class Cards():
    icons64 = {'hp': pg.image.load(path('Images/cards/hp64.png')).convert_alpha(),
               'hp_special': pg.image.load(path('Images/cards/hp_special64.png')).convert_alpha(),
               'stamina': pg.image.load(path('Images/cards/stamina64.png')).convert_alpha(),
               'stamina_special': pg.image.load(path('Images/cards/stamina_special64.png')).convert_alpha(),
               'dodge': pg.image.load(path('Images/cards/dodge64.png')).convert_alpha(),
               'dodge_special': pg.image.load(path('Images/cards/dodge_special64.png')).convert_alpha(),
               'resurrection': pg.image.load(path('Images/cards/resurrection64.png')).convert_alpha(),
               'resurrection_special': pg.image.load(path('Images/cards/resurrection_special64.png')).convert_alpha(),
               'shield': pg.image.load(path('Images/cards/shield64.png')).convert_alpha(),
               'shield_special': pg.image.load(path('Images/cards/shield_special64.png')).convert_alpha(),
               'penetration': pg.image.load(path('Images/cards/penetration64.png')).convert_alpha(),
               'penetration_special': pg.image.load(path('Images/cards/penetration_special64.png')).convert_alpha(),
               'atkDMG': pg.image.load(path('Images/cards/atkDMG64.png')).convert_alpha(),
               'atkDMG_special': pg.image.load(path('Images/cards/atkDMG_special64.png')).convert_alpha(),
               'atkSPD': pg.image.load(path('Images/cards/atkSPD64.png')).convert_alpha(),
               'atkSPD_special': pg.image.load(path('Images/cards/atkSPD_special64.png')).convert_alpha(),
               'ignite': pg.image.load(path('Images/cards/ignite64.png')).convert_alpha(),
               'ignite_special': pg.image.load(path('Images/cards/ignite_special64.png')).convert_alpha(),
               'explosion': pg.image.load(path('Images/cards/explosion64.png')).convert_alpha(),
               'explosion_special': pg.image.load(path('Images/cards/explosion_special64.png')).convert_alpha(),
               }

    icons32 = {'hp': pg.image.load(path('Images/cards/hp32.png')).convert_alpha(),
               'hp_special': pg.image.load(path('Images/cards/hp_special32.png')).convert_alpha(),
               'stamina': pg.image.load(path('Images/cards/stamina32.png')).convert_alpha(),
               'stamina_special': pg.image.load(path('Images/cards/stamina_special32.png')).convert_alpha(),
               'dodge': pg.image.load(path('Images/cards/dodge32.png')).convert_alpha(),
               'dodge_special': pg.image.load(path('Images/cards/dodge_special32.png')).convert_alpha(),
               'resurrection': pg.image.load(path('Images/cards/resurrection32.png')).convert_alpha(),
               'resurrection_special': pg.image.load(path('Images/cards/resurrection_special32.png')).convert_alpha(),
               'shield': pg.image.load(path('Images/cards/shield32.png')).convert_alpha(),
               'shield_special': pg.image.load(path('Images/cards/shield_special32.png')).convert_alpha(),
               'penetration': pg.image.load(path('Images/cards/penetration32.png')).convert_alpha(),
               'penetration_special': pg.image.load(path('Images/cards/penetration_special32.png')).convert_alpha(),
               'atkDMG': pg.image.load(path('Images/cards/atkDMG32.png')).convert_alpha(),
               'atkDMG_special': pg.image.load(path('Images/cards/atkDMG_special32.png')).convert_alpha(),
               'atkSPD': pg.image.load(path('Images/cards/atkSPD32.png')).convert_alpha(),
               'atkSPD_special': pg.image.load(path('Images/cards/atkSPD_special32.png')).convert_alpha(),
               'ignite': pg.image.load(path('Images/cards/ignite32.png')).convert_alpha(),
               'ignite_special': pg.image.load(path('Images/cards/ignite_special32.png')).convert_alpha(),
               'explosion': pg.image.load(path('Images/cards/explosion32.png')).convert_alpha(),
               'explosion_special': pg.image.load(path('Images/cards/explosion_special32.png')).convert_alpha(),
               }

    def __init__(self) -> None:

        self.cards = ['hp', 'stamina', 'dodge', 'resurrection', 'shield',
                      'penetration', 'atkDMG', 'atkSPD', 'ignite', 'explosion']

        self.cards_types = {'attack': ['explosion', 'explosion_special',
                                       'penetration', 'penetration_special',
                                       'atkDMG', 'atkDMG_special',
                                       'atkSPD', 'atkSPD_special',
                                       'ignite', 'ignite_special'],
                            'defense': ['hp', 'hp_special',
                                        'stamina', 'stamina_special',
                                        'dodge', 'dodge_special',
                                        'resurrection', 'resurrection_special',
                                        'shield', 'shield_special']}

        self.current_cards = []

        self.max_cards = 2
        self.max_lvl = 4

        self.owned = {'hp': 0,
                      'stamina': 0,
                      'dodge': 0,
                      'resurrection': 0,
                      'shield': 0,
                      'penetration': 0,
                      'atkDMG': 0,
                      'atkSPD': 0,
                      'ignite': 0,
                      'explosion': 0,
                      'hp_special': 0,
                      'stamina_special': 0,
                      'dodge_special': 0,
                      'resurrection_special': 0,
                      'shield_special': 0,
                      'penetration_special': 0,
                      'atkDMG_special': 0,
                      'atkSPD_special': 0,
                      'ignite_special': 0,
                      'explosion_special': 0}
        self.types_owned = {'attack': [], 'defense': []}

        self.update_owned_cards()
        self.ready = False

    def create_cards(self):
        n = min(len(self.cards), 4)
        if n == 4:
            number = 0.4
        elif n == 3:
            number = 0.6
        elif n == 2:
            number = 0.8
        else:
            number = 1
        for card in sample(self.cards, n):
            self.current_cards.append(Button(UI.display_text(
                card), UI.fonts['m'], UI.half_width*number, UI.half_height, card, 'card', image=Cards.icons64[card]))
            self.current_cards.append(Button(UI.display_text(
                f'{card}_description'), UI.fonts['description'], UI.half_width*number, UI.half_height+50, 0, 'description'))
            for type, cards in self.cards_types.items():
                if card in cards:
                    self.current_cards.append(Button(UI.display_text(
                        type), UI.fonts['sm'], UI.half_width*number, UI.half_height-130, 0, 'description'))
                    break
            number += 0.4

    def draw(self, events):
        if self.current_cards:
            for card in self.current_cards:
                card.draw()
            self.draw_owned_cards()
            return self.get_card(events)
        return True

    def get_card(self, events):
        if not pg.mouse.get_pressed()[0]:
            self.ready = True
        if self.ready:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.current_cards:
                        act = button.collide()
                        if act:
                            if act.find('special') >= 0:
                                self.remove_special_card(act)
                            else:
                                self.remove_card(act)

                            for type, cards in self.types_owned.items():
                                if len(cards) >= self.max_cards:
                                    for card in self.cards_types[type]:
                                        if card.find('special') == -1 and card not in cards and card in self.cards:
                                            self.cards.remove(card)
                            self.update_owned_cards()
                            self.current_cards.clear()
                            return act
                    self.ready = False
                    return False

    def remove_special_card(self, card):
        self.owned[card] += 1
        for type, cards in self.cards_types.items():
            if card in cards:
                self.types_owned[type].insert(
                    self.types_owned[type].index(card.replace('_special', '')), card)
                self.types_owned[type].remove(card.replace('_special', ''))
        self.cards.remove(card)

    def remove_card(self, card):
        self.owned[card] += 1
        if self.owned[card] == 1:
            for type, cards in self.cards_types.items():
                if card in cards:
                    self.types_owned[type].append(card)
                    break
        if self.owned[card] >= self.max_lvl:
            self.cards.remove(card)
            self.cards.append(f'{card}_special')

    def update_owned_cards(self):
        self.surface_attack = pg.surface.Surface((128, 128), pg.SRCALPHA)
        self.surface_defense = pg.surface.Surface((128, 128), pg.SRCALPHA)

        bg_special = pg.surface.Surface((32, 32), pg.SRCALPHA)
        bg_special.fill(UI.colors['blue'])
        bg_special_lvl = pg.surface.Surface((8, 8), pg.SRCALPHA)
        bg_special_lvl.fill(UI.colors['blue'])

        text_attack = UI.fonts['sm'].render(
            UI.display_text('attack'), False, UI.colors['white'])
        text_defense = UI.fonts['sm'].render(
            UI.display_text('defense'), False, UI.colors['white'])
        rect_attack = text_attack.get_rect(center=(64, 16))
        rect_defense = text_defense.get_rect(center=(64, 16))

        self.surface_attack.blit(text_attack, rect_attack)
        self.surface_defense.blit(text_defense, rect_defense)

        surfaces = {'attack': self.surface_attack,
                    'defense': self.surface_defense}

        for type, surface in surfaces.items():
            x = 24
            y = 24
            for card in self.types_owned[type]:
                if card.find('special') >= 0:
                    surface.blit(bg_special, (x, 32))
                    lvl = 0
                else:
                    lvl = self.owned[card]
                for i in range(1, 4+1):
                    if lvl == 0:
                        surface.blit(bg_special_lvl, (y, 64))
                    k = 0 if lvl >= i else 1
                    pg.draw.rect(surface,
                                 UI.colors['white'], (y, 64, 8, 8), k, 2)
                    y += 8

                surface.blit(Cards.icons32[card], (x, 32))
                x += 48
                y += 16

            pg.draw.rect(surface,
                         UI.colors['white'], (24, 32, 32, 32), 1, 2)
            pg.draw.rect(surface,
                         UI.colors['white'], (72, 32, 32, 32), 1, 2)

    def draw_owned_cards(self):
        UI.screen.blit(self.surface_attack, (UI.half_width-50-128, 10))
        UI.screen.blit(self.surface_defense, (UI.half_width+50, 10))
