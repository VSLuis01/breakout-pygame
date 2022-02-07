from typing import Any
import os
import pygame
import Power
import songs
from Constant import SCREEN_WIDTH, SCREEN_HEIGHT, IMG_DIR

# ball colours
BALL_COLOR0 = pygame.image.load(os.path.join(IMG_DIR, 'bolinhaCinza.png'))
BALL_COLOR1 = pygame.image.load(os.path.join(IMG_DIR, 'bolinhaverde.png'))
BALL_COLOR2 = pygame.image.load(os.path.join(IMG_DIR, 'bolinhalilas.png'))
BALL_COLOR3 = pygame.image.load(os.path.join(IMG_DIR, 'bolinhavermelha.png'))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 14

        self.image = BALL_COLOR1

        self.rect = self.image.get_rect()
        self.rect.x = x - self.radius
        self.rect.y = y + 5

        # velocidade a bola
        self.speedX = 4
        self.speedY = -4
        self.speedMax = 5
        # tolerancia de pixel para colisao
        self.pixelTolerance = 12
        # forca da bola
        self.strength = 1
        self.strength_plus_time = 0
        self.strength_minus_time = 0
        self.speed_time = 0

    # movimentacao da bola e verificacao de colisoes com as paredes
    def moving(self, isMoving):
        if isMoving:
            # check for collision with walls
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.speedX *= -1
                songs.hitWindowSound.play()
            # check for collision with top and bottom of the screen
            if self.rect.top < 0:
                self.speedY *= -1
                songs.hitWindowSound.play()
            if self.rect.bottom > SCREEN_HEIGHT + self.radius + 3:
                return True

            self.rect.x += self.speedX
            self.rect.y += self.speedY
        return False

    # colisao com os tijolos e com a plataforma
    def collision(self, playerPaddle, wall, powers):
        # look for collision with paddle
        if self.rect.colliderect(playerPaddle.rect):
            # check if colliding from the top
            if abs(self.rect.bottom - playerPaddle.rect.top) < self.pixelTolerance and self.speedY > 0:
                self.speedY *= -1
                self.speedX += playerPaddle.direction
                if self.speedX > self.speedMax:
                    self.speedX = self.speedMax
                elif self.speedX < 0 and self.speedX < -self.speedMax:
                    self.speedX = -self.speedMax
                playerPaddle.rect.y += 5
            # colisao com os lados
            else:
                self.speedX *= -1
            songs.hitPaddleSound.play()
        else:
            playerPaddle.rect.y = playerPaddle.y

        # collision with bricks
        for row in wall.bricks:
            for brick in row:
                # check collision
                if self.rect.colliderect(brick.rect) and brick.destroyed is False:
                    # check if collision was from above
                    if abs(self.rect.bottom - brick.rect.top) < self.pixelTolerance and self.speedY > 0:
                        self.speedY *= -1
                        brick.rect.y += 3
                    # check if collision was from below
                    if abs(self.rect.top - brick.rect.bottom) < self.pixelTolerance and self.speedY < 0:
                        self.speedY *= -1
                        brick.rect.y -= 3
                    # check if collision was from left
                    if abs(self.rect.right - brick.rect.left) < self.pixelTolerance and self.speedX > 0:
                        self.speedX *= -1
                        brick.rect.x -= 3
                    # check if collision was from right
                    if abs(self.rect.left - brick.rect.right) < self.pixelTolerance and self.speedX < 0:
                        self.speedX *= -1
                        brick.rect.x += 3
                    songs.hitBrickSound.play()
                    # reduce de block's strength by doing damage to it
                    if brick.strength > self.strength:
                        brick.strength -= self.strength
                    else:
                        brick.destroyed = True

                        # verificando se alguma brick tem algum power: buff ou debuff
                        if brick.powerType[0] == 1:
                            powers.append([Power.Buff(brick.rect.x, brick.rect.y, brick.power[0]), self])
                        elif brick.powerType[0] == -1:
                            powers.append([Power.DeBuff(brick.rect.x, brick.rect.y, brick.power[0]), self])

                        wall.bricksRemaining -= 1
                else:
                    brick.rect.y = brick.backupY
                    brick.rect.x = brick.backupX

    # atualiza a corda bola de acordo com a sua forca
    def update(self, *args: Any, **kwargs: Any):
        if self.strength == 1:
            self.image = BALL_COLOR1
        elif self.strength == 2:
            self.image = BALL_COLOR2
        elif self.strength == 3:
            self.image = BALL_COLOR3
        else:
            self.image = BALL_COLOR0

    # inicia o tempo de cada buff ou debuff
    def startTimer(self, power):
        if power == Power.BuffType.INCREASE_BALL_STRENGTH:
            self.strength_plus_time = pygame.time.get_ticks()
        elif power == Power.DeBuffType.INCREASE_BALL_SPEED:
            self.speed_time = pygame.time.get_ticks()
        elif power == Power.DeBuffType.DECREASE_BALL_STRENGTH:
            self.strength_minus_time = pygame.time.get_ticks()

    # veirifica se o tempo de algum buff acabou para resetar
    def powersTimer(self):
        if self.strength_plus_time != 0:
            seconds = (pygame.time.get_ticks() - self.strength_plus_time) / 1000
            if seconds > 15:
                self.strength = 1
                self.strength_plus_time = 0
        if self.speed_time != 0:
            seconds = (pygame.time.get_ticks() - self.speed_time) / 1000
            if seconds > 7:
                self.speedX = self.speedX / 1.6
                self.speedY = self.speedY / 1.6
                self.speedMax = 5
                self.speed_time = 0
        if self.strength_minus_time != 0:
            seconds = (pygame.time.get_ticks() - self.strength_minus_time) / 1000
            if seconds > 7:
                self.strength = 1
                self.strength_minus_time = 0

    # copia de uma bola para outra
    def copyBall(self, ball):
        self.speedX = ball.speedX
        self.speedY = ball.speedY
        self.speedMax = ball.speedMax
        self.strength = ball.strength
        self.strength_plus_time = ball.strength_plus_time
        self.strength_minus_time = ball.strength_minus_time
        self.speed_time = ball.speed_time

    def setPosition(self, x, y):
        self.rect.x = x - self.radius
        self.rect.y = y - 5

    # reseta os atributos
    def reset(self):
        self.speedX = 4
        self.speedY = -4
        self.speedMax = 5
        self.strength = 1
        self.strength_plus_time = 0
        self.strength_minus_time = 0
        self.speed_time = 0
