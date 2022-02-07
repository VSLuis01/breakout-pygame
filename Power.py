import enum
import pygame
import os
from Constant import IMG_DIR


# possiveis buffs
class BuffType(enum.Enum):
    INCREMENT_BALL = '+ball'
    INCREASE_PADDLE_SIZE = '+size'
    INCREASE_BALL_STRENGTH = '+strength'
    INCREASE_LIFE = '+life'


DEBUFF_IMAGE = pygame.image.load(os.path.join(IMG_DIR, 'poder1.png'))
BUFF_IMAGE = pygame.image.load(os.path.join(IMG_DIR, 'podebom.png'))


class Buff(pygame.sprite.Sprite):
    def __init__(self, x, y, buff):
        super().__init__()
        self.color = (0, 255, 0)
        self.type = buff
        self.buffTime = 0

        self.image = BUFF_IMAGE

        self.rect = self.image.get_rect()
        self.rect.x = x + self.image.get_width() // 2
        self.rect.y = y

        # tempo dos buffs
        if self.type == BuffType.INCREASE_PADDLE_SIZE:
            self.buffTime = 15
        elif self.type == BuffType.INCREASE_BALL_STRENGTH:
            self.buffTime = 18

    # colisao com o player (plataforma)
    def updatePower(self, paddle):
        self.rect.y += 2
        if self.rect.colliderect(paddle.rect):
            return True

        return False

    # renderiza os poderes
    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(window, self.color, self.rect)


class DeBuffType(enum.Enum):
    DECREASE_PADDLE_SIZE = '-size'
    DECREASE_BALL_STRENGTH = '-strength'
    INCREASE_BALL_SPEED = '+speed'
    DECREASE_LIFE = '-life'


class DeBuff(pygame.sprite.Sprite):
    def __init__(self, x, y, debuff):
        super().__init__()
        self.color = (255, 0, 0)
        self.buffTime = 7
        self.type = debuff

        self.image = DEBUFF_IMAGE

        self.rect = self.image.get_rect()
        self.rect.x = x + self.image.get_width() // 2
        self.rect.y = y

    def updatePower(self, paddle):
        self.rect.y += 3
        if self.rect.colliderect(paddle.rect):
            return True

        return False

    def render(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(window, self.color, self.rect)
