import pygame as pg
from settings import UI


class Rank():
    def __init__(self):
        self.order = ['pos', 'nickname', 'score']

    def render_table(self, data, save):
        if not data:
            data = []
        self.surface = pg.surface.Surface(UI.screen.get_size(), pg.SRCALPHA)
        self.top = UI.half_height-300
        self.y = 0

        header = {'pos': UI.display_text('pos'), 'nickname': UI.display_text(
            'nickname'), 'score': UI.display_text('score')}
        self.write_row(header, UI.fonts['l'])
        self.y -= 15

        self.draw_line((UI.half_width/3, self.top+self.y),
                       (5*UI.half_width/3, self.top+self.y))

        while len(data) < 10:
            data.append({'pos': '-', 'nickname': '-', 'score': '-'})
        for item in data:
            if isinstance(item['pos'], int):
                if item['pos'] > 10:
                    break
                item['score'] = self.format_score(item['score'])
            self.write_row(item, UI.fonts['m'])
        self.y -= 15

        self.draw_line((UI.half_width/3, self.top+self.y),
                       (5*UI.half_width/3, self.top+self.y))

        for item in data:
            if item['nickname'] == save['nickname']:
                self.write_row(item, UI.fonts['m'])

        return self.surface

    def format_score(self, score):
        minutes = score // 60
        score %= 60
        return f"{minutes:02d}:{score:02d}"

    def write_row(self, dict, font):
        column = 0.25
        for i in range(len(dict)):
            row_surface = font.render(
                str(dict[self.order[i]]), True, UI.colors['white'])
            row_rect = row_surface.get_rect(
                center=(UI.dimension[0]*column, self.top+self.y))
            self.surface.blit(row_surface, row_rect)
            column += 0.25
        self.y += 40

    def draw_line(self, start, end):
        pg.draw.line(self.surface, UI.colors['light-blue'], start, end, 2)
        self.y += 25
