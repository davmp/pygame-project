import pygame

import config

pygame.font.init()


class Text:
    def __init__(self, posx, posy, string, color, size, font=config.font):
        self.posx = posx
        self.posy = posy
        self.string = string
        self.color = color
        self.size = size
        self.font = pygame.font.Font(font, self.size)
        self.layout = self.font.render(self.string, True, self.color)

    def draw(self, canvas):
        canvas.blit(self.layout, (self.posx, self.posy))

    def update_string(self, string):
        self.layout = self.font.render(string, True, self.color)
        self.string = string

    def update_pos(self, x, y):
        self.posx = x
        self.posy = y
