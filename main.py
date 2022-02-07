import pygame
import Ball
import Paddle
import Power
import Wall
import Text
import os
import menu
from Constant import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, GameOverTypes, IMG_DIR

# initialize screen
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout')

# imagem do ifonce
ICON_IMAGE = pygame.image.load(os.path.join(IMG_DIR, 'icon.png'))
pygame.display.set_icon(ICON_IMAGE)

# imagem de fundo da batalha
BACK_GROUND_DIR = pygame.image.load(os.path.join(IMG_DIR, 'fundLuis.png')).convert()
backGround = pygame.sprite.Sprite()
backGround.image = BACK_GROUND_DIR
backGround.rect = BACK_GROUND_DIR.get_rect()

# musica da batalha
chanel0 = pygame.mixer.Channel(0)
gameMusic = pygame.mixer.Sound('sounds/battle_music.ogg')

# maximum FPS
clock = pygame.time.Clock()
fps = 60
# game variables
ballMoving = False
pause = False
# game over define varios estados do game
gameOver = GameOverTypes.NOT_START


# inicia o timer dos poderes
def powersTimerCount():
    for ball in balls:
        ball.powersTimer()

    player.powersTimer()


# aplica os buffs ou debuffs
def applyPower(buff):
    # buff de aumentar quantidade de bolas
    if buff[0].type == Power.BuffType.INCREMENT_BALL:
        newBall = Ball.Ball(buff[1].rect.x, buff[1].rect.y)
        newBall.copyBall(buff[1])
        balls.append(newBall)
        allSprites.add(balls)

    # buff de aumentar a forca da bola
    elif buff[0].type == Power.BuffType.INCREASE_BALL_STRENGTH:
        if buff[1].strength < 3:
            buff[1].strength += 1
            buff[1].startTimer(buff[0].type)

    # buff de auemntar o tamanho da plataforma
    elif buff[0].type == Power.BuffType.INCREASE_PADDLE_SIZE:
        player.increaseWidth()
        player.startTimer(buff[0].type)

    # buff de aumentara q auantidade de vida
    elif buff[0].type == Power.BuffType.INCREASE_LIFE:
        player.lives += 1

    # debuff diminui a forca da bola
    elif buff[0].type == Power.DeBuffType.DECREASE_BALL_STRENGTH:
        if buff[1].strength >= 1:
            buff[1].strength -= 1
            buff[1].startTimer(buff[0].type)

    # debuff diminui o tamanho da plataforma
    elif buff[0].type == Power.DeBuffType.DECREASE_PADDLE_SIZE:
        player.decreaseWidth()
        player.startTimer(buff[0].type)

    # debuff / buff aumenta a velocidade da bola
    elif buff[0].type == Power.DeBuffType.INCREASE_BALL_SPEED:
        buff[1].speedX = buff[1].speedX * 1.6
        buff[1].speedY = buff[1].speedY * 1.6
        buff[1].speedMax = buff[1].speedMax * 2
        buff[1].startTimer(buff[0].type)

    # debuff diminui a quantidade de vida
    elif buff[0].type == Power.DeBuffType.DECREASE_LIFE:
        player.lives -= 1


# renderiza os objetos
def render():
    window.fill(BACKGROUND_COLOR)
    allSprites.draw(window)
    # desenha a parede de tijolos
    wallOfBricks.drawWall(window)
    # desenha a plataforma
    player.draw(window)
    # desenha as bolas
    for power in powers:
        power[0].render(window)


# atualizacoes do jogo (movimento de plataforma, bola, contagem de pontos, etc).
def update():
    if pause is False:
        allSprites.update()
        global gameOver
        # movimentacao da pltaforma
        if gameOver != GameOverTypes.LOST and gameOver != GameOverTypes.WIN:
            player.move()

        # atualizacao das bolas
        if gameOver != GameOverTypes.NOT_START and gameOver != GameOverTypes.LOST:
            for ball in balls:
                off_the_window = ball.moving(ballMoving)
                if off_the_window and len(balls) > 1:
                    gameOver = GameOverTypes.CONTINUE
                    allSprites.remove(ball)
                    balls.pop(balls.index(ball))
                elif off_the_window and len(balls) <= 1:
                    gameOver = GameOverTypes.SECOND_CHANCE
                else:
                    gameOver = GameOverTypes.CONTINUE

        # se a bola nao esta movendo, reseta a sua posicao
        if not ballMoving:
            powers.clear()
            balls[0].reset()
            balls[0].setPosition(player.rect.x + (player.width // 2), player.rect.y - player.height)
        else:
            powersTimerCount()
            # colisao das bolas
            for ball in balls:
                ball.collision(player, wallOfBricks, powers)
            # colisao dos poderes com a plataforma
            for power in powers:
                catchPower = power[0].updatePower(player)
                if catchPower is True:
                    powers.pop(powers.index(power))
                    applyPower(power)
                elif power[0].rect.y > SCREEN_HEIGHT + power[0].rect.height:
                    powers.pop(powers.index(power))

        # se acabou os tijolos, o jogador ganha
        if wallOfBricks.bricksRemaining == 0:
            gameOver = GameOverTypes.WIN

        # se acabou as vidas o jogador perde
        if player.lives == 0:
            gameOver = GameOverTypes.LOST


# menu principal
menu = menu.Menu(window)
running = menu.run()

# muro de bricks
wallOfBricks = Wall.Wall()
wallOfBricks.createWall()

# plataforma do jogador
player = Paddle.Paddle()

# bola
mainBall = Ball.Ball(player.rect.x + (player.width // 2), player.rect.y - player.height)
balls = [mainBall]

# texto de instrucao
text = Text.Text('Crayone.otf', 46)
text.setColor((222, 184, 224))

powers = []

allSprites = pygame.sprite.Group()
allSprites.add(backGround, balls)

chanel0.play(gameMusic, -1)
chanel0.set_volume(0.5)

while running:

    # desenha tudo o que é renderizavel
    render()
    # atualiza todos elementos que se movem
    update()

    if gameOver == GameOverTypes.SECOND_CHANCE:
        player.lives -= 1
        ballMoving = False
        text.setStringText('')
    elif gameOver == GameOverTypes.WIN:
        text.setStringText('YOU WIN!')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 100)
        text.draw(window)
        text.setStringText('PRESS SPACE TO RESTART')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 150)
        text.draw(window)
        ballMoving = False
    elif gameOver == GameOverTypes.LOST:
        text.setStringText('GAME OVER!')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 100)
        text.draw(window)
        text.setStringText('PRESS SPACE TO RESTART')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 150)
        text.draw(window)
        ballMoving = False

    if gameOver == GameOverTypes.NOT_START:
        text.setStringText('CLICK TO LAUNCH')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 100)
        text.draw(window)

    if pause is True:
        # ballMoving = False
        text.setStringText('PAUSE')
        text.setPosition(SCREEN_WIDTH // 2 - text.width // 2, SCREEN_HEIGHT // 2 + 100)
        text.draw(window)
        chanel0.pause()
    else:
        chanel0.unpause()

    # pilha de eventos
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        # pause
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause = True if pause is False else False
        # click mouse 1 para lancar a bola
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # botao do mouse para lançar
            if event.button == 1:
                if ballMoving is False and gameOver != GameOverTypes.LOST and gameOver != GameOverTypes.WIN:
                    ballMoving = True
                    gameOver = GameOverTypes.CONTINUE

    # espaço para reiniciar
    if pygame.key.get_pressed()[pygame.K_SPACE] and ballMoving is False:
        if gameOver == GameOverTypes.LOST or gameOver == GameOverTypes.WIN:
            allSprites.empty()
            wallOfBricks.createWall()
            player.reset()
            balls.clear()
            balls.append(mainBall)
            balls[0].reset()
            gameOver = GameOverTypes.NOT_START
            allSprites.add(backGround, balls)

    clock.tick(fps)
    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
