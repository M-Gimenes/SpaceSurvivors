from settings import UI


class Text:
    def __init__(self, content: str, font: str, pos: tuple, max_width: int) -> None:
        self.BUTTONSTATES = {
            True:UI.colors['light-blue'],
            False:UI.colors['white']
        }

        self.font = font
        self.content = content
        self.pos = pos
        self.max_width = max_width

    def render(self, scale = 1, selected = False):
        y = 0
        for line in self.divide_line():
            text_surface = self.font.render(line, False, self.BUTTONSTATES[selected])
            rect = text_surface.get_rect(center = (self.pos[0]+1,self.pos[1]+2+y))
            UI.screen.blit(text_surface, rect)
            y += text_surface.get_height() + 5

    def divide_line(self):
        words = self.content.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            test_width, _ = self.font.size(test_line)

            if test_width <= self.max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines