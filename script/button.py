import pygame as pg
from settings import UI
from text import Text


class Button():
    def __init__(self, text: str, font: pg.font.Font, x: int, y: int, action, type: str, image=None) -> None:
        width, height = font.size(text)
        if width < height:
            width = height
        if type in ['card', 'description']:
            self.border = pg.Rect(0, 0, 200, 300)
            self.text = Text(text, font, (x, y), 180)
            self.contrast = pg.surface.Surface((200, 300), pg.SRCALPHA)
            if image:
                self.image = image
        else:
            self.border = pg.Rect(0, 0, width+10, height+10)
            self.text = Text(text, font, (x, y), width)
            self.contrast = pg.surface.Surface(
                (width+10, height+10), pg.SRCALPHA)
            self.arrowleft = [(x-width/2-50, y), (x-width /
                                                  2-20-50, y-10), (x-width/2-20-50, y+10)]
            self.arrowright = [
                (x+width/2+50, y), (x+width/2+20+50, y-10), (x+width/2+20+50, y+10)]

        self.border.center = (x, y)
        self.type = type
        self.action = action
        self.contrast.fill((255, 255, 255, 25))

    def draw(self) -> None:
        if self.type == 'button':
            pg.draw.rect(UI.screen, (UI.colors['blue']), self.border, 0, 2)
            pg.draw.rect(UI.screen, (UI.colors['white']), self.border, 2, 2)
            if self.border.collidepoint(pg.mouse.get_pos()):
                UI.screen.blit(self.contrast, self.border)
        elif self.type == 'card':
            if self.action.find('special') >= 0:
                pg.draw.rect(UI.screen, (UI.colors['blue']), self.border, 0, 2)
            else:
                pg.draw.rect(
                    UI.screen, (UI.colors['black']), self.border, 0, 2)
            pg.draw.rect(UI.screen, (UI.colors['white']), self.border, 2, 2)
            if self.border.collidepoint(pg.mouse.get_pos()):
                UI.screen.blit(self.contrast, self.border)
            UI.screen.blit(
                self.image, (self.border[0]+100-self.image.get_width()/2, self.border[1] + 50))

        if self.type == 'menu' and self.border.collidepoint(pg.mouse.get_pos()):
            self.text.render(1.25, True)
            pg.draw.aalines(
                UI.screen, (UI.colors['white']), True, self.arrowleft)
            pg.draw.aalines(
                UI.screen, (UI.colors['white']), True, self.arrowright)
        else:
            self.text.render()

    def collide(self):
        if self.border.collidepoint(pg.mouse.get_pos()):
            return self.action
        return False
