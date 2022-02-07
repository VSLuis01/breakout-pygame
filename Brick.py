import pygame
import numpy
import Power
from Constant import SCREEN_WIDTH, COLUM_NUM, BACKGROUND_COLOR

# define block colours
import Text

BLOCK3_COLOR = (84, 48, 84)
BLOCK2_COLOR = (140, 104, 140)
BLOCK1_COLOR = (184, 149, 172)


class Brick(pygame.Surface):
    def __init__(self, posX, posY, strength):
        self.width = SCREEN_WIDTH // COLUM_NUM - 2
        self.height = 50
        super().__init__((self.width, self.height))
        self.strength = strength

        # self.image = pygame.Surface((self.width, self.height))
        self.rect = self.get_rect()
        self.set_alpha(211)

        self.rect.x = posX * (self.width + 2) + 1
        self.rect.y = posY * (self.height + 2) + 1

        # powerUps que a brick pode ter
        self.powerUps = [-1, 0, 1] #-1 debuff 0 normal 1 buff
        self.powerType = []
        self.power = []

        self.destroyed = False

        # texto do poder que contem em cada brick
        self.text = Text.Text('constan.ttf', 20)
        self.text.setStringText('')
        self.text.setColor((247, 230, 225))

        self.backupX = self.rect.x
        self.backupY = self.rect.y

        if strength == 3:
            # define a probabilidade de uma brick ter um debuff/normal/buff
            self.powerType = numpy.random.choice(self.powerUps, 1, p=[0.10, 0.75, 0.15])
            self.color = BLOCK3_COLOR
        elif strength == 2:
            self.powerType = numpy.random.choice(self.powerUps, 1, p=[0.15, 0.60, 0.25])
            self.color = BLOCK2_COLOR
        else:
            self.powerType = numpy.random.choice(self.powerUps, 1, p=[0.05, 0.70, 0.25])
            self.color = BLOCK1_COLOR

        self.fill(self.color)
        # selecionando um buff ou debuff
        # debuff
        if self.powerType[0] == -1:
            debuffs = []
            for debuff in Power.DeBuffType:
                debuffs.append(debuff)
            self.power = numpy.random.choice(debuffs, 1, p=[0.25, 0.25, 0.25, 0.25])
        # buff
        elif self.powerType[0] == 1:
            buffs = []
            for buff in Power.BuffType:
                buffs.append(buff)
            self.power = numpy.random.choice(buffs, 1, p=[0.30, 0.20, 0.35, 0.15])

    def draw(self, window):
        # verificando se alguma brick tem algum power: buff ou debuff
        # define a cor das bricks de acordo com o tanto de vida q elas tem
        if self.strength == 3:
            self.color = BLOCK3_COLOR
        elif self.strength == 2:
            self.color = BLOCK2_COLOR
        else:
            self.color = BLOCK1_COLOR
        self.fill(self.color)

        if self.destroyed is False:
            if len(self.power) > 0:
                self.text.setStringText(self.power[0].value)

            window.blit(self, (self.rect.x, self.rect.y))
            self.text.setPosition(self.rect.x + self.width // 2 - (self.text.width // 2), self.rect.y + 15)
            self.text.draw(window)
