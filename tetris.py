import pygame
import Queue
import math
from random import randint
import numpy as np

Black = (0, 0, 0)

Colour = { 0 : (150, 150, 150), # None
           1 : (0, 150, 150),   # I
           2 : (150, 150, 0),   # O
           3 : (150, 0, 0),     # Z
           4 : (0, 150, 0),     # S
           5 : (200, 130, 0),   # L
           6 : (0, 0, 150),     # J
           7 : (150, 0, 150) }  # T

TPieceCoord = { 1 : np.array([ (0, -1), (0, 0), (0, 1), (0, 2)]), # I
                2 : np.array([ (0, 0), (1, 0), (0, 1), (1, 1)]),  # O
                3 : np.array([ (-1, 0), (0, 0), (0, 1), (1, 1)]),  # Z
                4 : np.array([ (-1, 1), (0, 1), (0, 0), (1, 0)]),  # S
                5 : np.array([ (0, -1), (0, 0), (0, 1), (1, 1)]),  # L
                6 : np.array([ (0, -1), (0, 0), (0, 1), (-1, 1)]),  # J
                7 : np.array([ (-1, 0), (0, 0), (1, 0), (0, -1)]) } # T

#Line block:
# O
# O
# O
# O
Teal = (0, 150, 150)
iBlock = 1

# Square block:
# OO
# OO
Yellow = (150, 150, 0)
oBlock = 2

# Z block:
# OO
#  OO
Red = (150, 0, 0)
zBlock = 3

# S block:
#  OO
# OO
Grean = (0, 150, 0)
sBlock = 4

# L block:
# O
# O
# OO
Orange = (200, 130, 0)
lBlock = 5

# J block:
#  O
#  O
# OO
Blue = (0, 0, 150)
jBlock = 6

# T Block:
#  O
# OOO
Purple = (150, 0, 150)
tBlock = 7

class TetrisPiece():
    def __init__(self, grid):
        self.type = randint(1, 7)
        self.grid = grid
        self.center = np.array([int(math.floor(grid.width/2)), grid.height - 1])
        self.blocks = self.generatePieces()
        self.fitInGrid()

    def generatePieces(self):
        return TPieceCoord[self.type] + self.center

    def fitInGrid(self):
        yOutBound = self.grid.height - 1
        for block in self.blocks:
            if block[1] > yOutBound:
                yOutBound = block[1]

        yShift = yOutBound - self.grid.height + 1

        if yShift != 0:
            self.blocks -= (0, yShift)
            self.center -= (0, yShift)

    def movePiece(direction):
        self.blocks += direction
        self.center += direction

    def draw(self, screen):
        for block in self.blocks:
            self.grid.drawBlock(screen, block[0], block[1], self.type)

class TetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10

        self.cells = []
        self.activePiece = TetrisPiece(self) #None
        self.pieceQueue = Queue.Queue()

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.xOffset = (screenWidth - self.width * self.size) / 2
        self.yOffset = (screenHeight - self.height * self.size) / 2

    def realCoord(self, x, y):
        return (x * self.size + self.xOffset, y * self.size + self.yOffset)

    def drawGrid(self, screen):
        for y in range(0, self.height + 1):
            pygame.draw.line(screen, Black, self.realCoord(0, y), self.realCoord(self.width, y))
        for x in range(0, self.width + 1):
            pygame.draw.line(screen, Black, self.realCoord(x, 0), self.realCoord(x, self.height))

    def drawBlocks(self, screen):
        h = 0
        cut = len(self.cells)
        while (h < self.height):
            if (h < cut):
                for x in range(0, self.width):
                    self.drawBlock(screen, x, h, self.cells[h][x])
            else:
                for x in range(0, self.width):
                    self.drawBlock(screen, x, h, 0)
            h += 1

    def drawBlock(self, screen, x, h, col):
        y = self.height - h - 1
        block = pygame.rect.Rect(self.realCoord(x, y),(self.size, self.size))
        pygame.draw.rect(screen, Colour[col], block, 0)



    def draw(self, screen):
        self.drawBlocks(screen)
        self.activePiece.draw(screen)
        self.drawGrid(screen)

class Game(object):
    #def __init__(self):

    def draw(self, screen):
        screen.fill((200, 200, 200))
        self.grid.draw(screen)
        pygame.display.flip()
        
    def main(self, screen):
        self.grid = TetrisGrid(screen)

        while 1:
            clock = pygame.time.Clock()

            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.draw(screen)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
