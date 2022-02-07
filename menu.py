import pygame
import os
import button
from Constant import IMG_DIR, SONGS_DIR

music = pygame.mixer.Sound(os.path.join(SONGS_DIR, 'menu_music.mp3'))
music.set_volume(0.35)


# menu principal para jogar ou sair
class Menu:
    def __init__(self, window):
        # botao start
        self.buttonStart = button.Button(200, 70, 195, 300)
        self.buttonStart.setColor(255, 255, 255, 128)
        self.buttonStart.setTextColor((253, 243, 240))
        self.buttonStart.setText('PLAY')

        # botar quit
        self.buttonQuit = button.Button(205, 68, 195, 405)
        self.buttonQuit.setColor(255, 255, 255, 128)
        self.buttonQuit.setTextColor((253, 243, 240))
        self.buttonQuit.setText('QUIT')

        self.backGround = pygame.image.load(os.path.join(IMG_DIR, 'menuFund.png'))

        self.running = True
        self.start = False
        self.window = window

    def render(self):
        self.window.blit(self.backGround, (0, 0))
        self.buttonStart.draw(self.window)
        self.buttonQuit.draw(self.window)

    # atualiza a cor dos botoes, caso a mouse fica em cima
    def updateButtons(self):
        if self.buttonStart.contains(pygame.mouse.get_pos()):
            self.buttonStart.setColor(255, 255, 255, 40)
        else:
            self.buttonStart.setColor(255, 255, 255, 0)

        if self.buttonQuit.contains(pygame.mouse.get_pos()):
            self.buttonQuit.setColor(255, 255, 255, 40)
        else:
            self.buttonQuit.setColor(255, 255, 255, 0)

    def pollEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # botao do mouse para lançar
                if event.button == 1:
                    if self.buttonStart.gotClicked(pygame.mouse.get_pos()):
                        self.start = True
                        self.running = False
                    if self.buttonQuit.gotClicked(pygame.mouse.get_pos()):
                        self.start = False
                        self.running = False

    def update(self):
        self.updateButtons()
        self.pollEvent()

    # loop principal do menu
    def run(self):
        music.play(-1)
        while self.running:
            self.render()
            self.update()
            pygame.display.flip()

        music.stop()
        return self.start
