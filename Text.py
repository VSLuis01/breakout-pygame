import pygame
import os

gameFolder = os.path.dirname(__file__)
fontsFolder = os.path.join(gameFolder, 'fonts')


# classe que representa qualquer texto
class Text:
    def __init__(self, font, size):
        self.fontSize = size
        self.fontName = os.path.join(fontsFolder, font)
        self.font = pygame.font.Font(self.fontName, self.fontSize)
        self.text = ''
        self.width, self.height = self.font.size(self.text)
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)

    # texto da string
    def setStringText(self, string):
        self.text = string
        self.width, self.height = self.font.size(self.text)

    # posicao do texto
    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setColor(self, color):
        self.color = color

    def setFontSize(self, size):
        self.fontSize = size
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)

    def draw(self, window):
        img = self.font.render(self.text, True, self.color)
        window.blit(img, (self.x, self.y))
