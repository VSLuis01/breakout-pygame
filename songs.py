import pygame
pygame.mixer.init()


hitBrickSound = pygame.mixer.Sound('sounds/hit_brick.wav')
hitBrickSound.set_volume(0.2)
hitPaddleSound = pygame.mixer.Sound('sounds/hit_paddle.wav')
hitPaddleSound.set_volume(0.2)
hitWindowSound = pygame.mixer.Sound('sounds/hit_window.wav')
hitWindowSound.set_volume(0.2)
