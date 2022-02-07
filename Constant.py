from enum import Enum
import os

BACKGROUND_COLOR = (111, 111, 111)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

COLUM_NUM = 6
ROW_NUM = 6

GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, 'img')
SONGS_DIR = os.path.join(GAME_DIR, 'sounds')

class GameOverTypes(Enum):
    NOT_START = 0
    CONTINUE = 1
    SECOND_CHANCE = 2
    WIN = 3
    LOST = -1
