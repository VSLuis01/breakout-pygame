import pygame
import Text


# classe que representa algum bota do jogo
class Button(pygame.Surface):
    def __init__(self, width, height, x, y):
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = (255, 0, 0)
        self.fill(self.color)
        self.text = Text.Text('Crayone.otf', 42)
        self.centerText()

    def centerText(self):
        self.text.setPosition(self.rect.x + self.text.width // 2, self.rect.y + self.rect.height / 2 - 28)

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.text.setPosition(self.rect.width // 2 + self.text.width // 2 + 10,
                              self.rect.y + self.text.height - 5)

    def setText(self, text):
        self.text.setStringText(text)
        self.centerText()

    def setTextSize(self, size):
        self.text.setFontSize(size)

    def setTextColor(self, color):
        self.text.setColor(color)

    def setColor(self, R, G, B, A):
        self.color = (R, G, B)
        self.fill(self.color)
        self.set_alpha(A)

    def draw(self, window):
        window.blit(self, (self.rect.x, self.rect.y))
        # pygame.draw.rect(window, self.color, self)
        self.text.draw(window)

    def contains(self, mousePos):
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False

    def buttonUpdate(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = (150, 0, 0)
        else:
            self.color = (255, 0, 0)

    def gotClicked(self, pos):
        return self.rect.collidepoint(pos)
