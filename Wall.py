import Brick
from Constant import ROW_NUM, COLUM_NUM


class Wall:
    def __init__(self):

        self.bricks = []

        self.bricksRemaining = 0

    # cria a parede de tijolos (Bricks)
    def createWall(self):
        self.bricks = []
        for row in range(ROW_NUM):
            # reinicia a lista de blocos na linha
            brickRow = []
            for colum in range(COLUM_NUM):
                # força do brick
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                else:
                    strength = 1
                # gera a posica x e y da brick
                brick = Brick.Brick(colum, row, strength)
                # adiciona um brick na linha
                brickRow.append(brick)
            # adiciona a linha de bricks para lista de todas as brick
            self.bricks.append(brickRow)
        # quantidade de bricks
        self.bricksRemaining = len(self.bricks) * len(self.bricks[0])

    # deseja os a parede com os tijolos
    def drawWall(self, window):
        for row in self.bricks:
            for brick in row:
                # desenha o brick
                brick.draw(window)
