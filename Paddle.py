import pygame

import Power
import Text
from Constant import SCREEN_WIDTH

# paddle colours
PADDLE_COLOR = (28, 6, 21)
PADDLE_OUTLINE_COLOR = (142, 106, 130)


# a plataforma eh uma surface para poder ser transparente
class Paddle(pygame.Surface):
    def __init__(self):
        self.height = 20
        self.widthFactor = 6
        self.width = int(SCREEN_WIDTH / self.widthFactor)
        super().__init__((self.width, self.height))

        self.fill(PADDLE_COLOR)
        self.set_alpha(0)

        # posicao inicial x
        self.x = int((SCREEN_WIDTH / 2) - (self.width / 2))
        # posicao inicial y
        self.y = SCREEN_WIDTH - (self.height * 2)

        self.rect = self.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.lives = 3
        self.speed = 10
        self.direction = 0

        self.text = Text.Text('constan.ttf', 20)
        self.text.setColor((247, 230, 225))

        # timers dos poderes
        self.size_plus_timer = 0
        self.size_minus_timer = 0

    # movimentacao da plataforma
    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        elif key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.direction = 1
        else:
            self.direction = 0

        self.text.setStringText(str(self.lives))
        self.text.setPosition(self.rect.x + self.width // 2 - (self.text.width // 2), self.rect.y - 3)

    def draw(self, window):
        window.blit(self, (self.rect.x, self.rect.y))
        pygame.draw.rect(window, PADDLE_OUTLINE_COLOR, self.rect, 3)
        self.text.draw(window)

    # verifica se o tempo dos buffs ou debuffs nao esgotou
    def powersTimer(self):
        if self.size_plus_timer != 0:
            seconds = (pygame.time.get_ticks() - self.size_plus_timer) / 1000
            if seconds > 15:
                self.resetWidth()
                self.size_plus_timer = 0
        if self.size_minus_timer != 0:
            seconds = (pygame.time.get_ticks() - self.size_minus_timer) / 1000
            if seconds > 10:
                self.resetWidth()
                self.size_minus_timer = 0

    # inicia o timer para os buffs e deffufs
    def startTimer(self, buff):
        if buff == Power.BuffType.INCREASE_PADDLE_SIZE:
            self.size_plus_timer = pygame.time.get_ticks()
        elif buff == Power.DeBuffType.DECREASE_PADDLE_SIZE:
            self.size_minus_timer = pygame.time.get_ticks()

    # aumenta o comprimento da plataforma
    def increaseWidth(self):
        if self.widthFactor > 2:
            self.widthFactor -= 2
        self.width = int(SCREEN_WIDTH / self.widthFactor)
        self.fill(PADDLE_COLOR)
        self.rect.update(self.rect.x, self.y, self.width, self.height)

    # diminui o comprimento da plataforma
    def decreaseWidth(self):
        if self.widthFactor < 9:
            self.widthFactor += 2
        self.width = int(SCREEN_WIDTH / self.widthFactor)
        self.fill(PADDLE_COLOR)
        self.rect.update(self.rect.x, self.y, self.width, self.height)

    # reseta o comprimento da plataforma
    def resetWidth(self):
        self.widthFactor = 6
        self.width = int(SCREEN_WIDTH / self.widthFactor)
        self.fill(PADDLE_COLOR)
        self.rect.update(self.rect.x, self.y, self.width, self.height)

    # reinicia os atributos da plataforma
    def reset(self):
        # define paddle variables
        self.widthFactor = 6
        self.width = int(SCREEN_WIDTH / self.widthFactor)
        self.rect.update(self.x, self.y, self.width, self.height)
        self.lives = 3
        self.direction = 0
        self.size_minus_timer = 0
        self.size_plus_timer = 0
