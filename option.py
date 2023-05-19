class Option():
    def _init_(self, pos, input, font, color, hover_color):
        self.font = font
        self.color, self.hovering_color = color, hover_color
        self.input = input
        self.text = self.font.render(self.input, True, self.color)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def displayInput(self, index):
        if index[0] in range(self.rect.left, self.rect.right) and index[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def doHover(self, index):
        if index[0] in range(self.rect.left, self.rect.right) and index[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.input, True, self.color)

    def update(self, gui):
        gui.blit(self.text, self.text_rect)
