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

TPieceCoord = { 1 : np.array([ (-1, 0), (0, 0), (1, 0), (2, 0)]), # I
                2 : np.array([ (0, -1), (1, -1), (0, 0), (1, 0)]),  # O
                3 : np.array([ (-1, 0), (0, 0), (0, -1), (1, -1)]),  # Z
                4 : np.array([ (-1, -1), (0, -1), (0, 0), (1, 0)]),  # S
                5 : np.array([ (-1, 0), (0, 0), (1, 0), (1, 1)]),  # L
                6 : np.array([ (-1, 1), (-1, 0), (0, 0), (1, 0)]),  # J
                7 : np.array([ (-1, 0), (0, 0), (1, 0), (0, -1)]) } # T

class TPieceControler():
    def __init__(self, tPiece = None):
        self.leftHeld = False
        self.rightHeld = False
        self.upHeld = False
        self.downHeld = False
        self.tPiece = tPiece

    def changePiece(self,tPiece):
        self.tPiece = tPiece

    def recieveInput(self):
        if self.tPiece is not None:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                if self.leftHeld == False:
                    self.tPiece.movePiece((-1, 0))
                    self.leftHeld = True
            else:
                self.leftHeld = False

            if key[pygame.K_RIGHT]:
                if self.rightHeld == False:
                    self.tPiece.movePiece((1, 0))
                    self.rightHeld = True
            else:
                self.rightHeld = False

            if key[pygame.K_UP]:
                if self.upHeld == False:
                    self.tPiece.rotate()
                    self.upHeld = True
            else:
                self.upHeld = False

            if key[pygame.K_DOWN]:
                if self.downHeld == False:
                    self.tPiece.movePiece((0, -1))
                    self.downHeld = True
            else:
                self.downHeld = False

class TetrisPiece():
    def __init__(self, grid):
        self.type = randint(1, 7)
        self.grid = grid

        beginningHeight = grid.height - 1
        gridCenter = int(math.floor(grid.width/2))
        if self.type in (5, 6):
            beginningHeight -= 1
        self.center = np.array([gridCenter, beginningHeight])

        self.blocks = TPieceCoord[self.type]

        self.readyToPlace = False

    def coord(self):
        return self.blocks + self.center

    def movePiece(self, direction):
        height = self.grid.height
        width = self.grid.width

        tempCenter = self.center + direction
        fix = self.enclose(tempCenter)
        if fix == (0, 0):
            self.center = tempCenter

        if fix[1] == -1:
            if self.readyToPlace:
                self.grid.placePiece()
            else:
                self.readyToPlace = True

    def rotate(self):
        for i in range(0, 4):
            x, y = self.blocks[i]
            self.blocks[i] = np.array([y, -x])
        fix = self.enclose()
        self.center -= fix
        self.readyToPlace = False


    def enclose(self, center = None):
        xMax = None
        xMin = None
        yMax = None
        yMin = None
        if center is None:
            center = self.center
        piece = self.blocks + center
        for block in piece:
            if xMax is None:
                xMax = block[0]
                xMin = block[0]
                yMax = block[1]
                yMin = block[1]
            else:
                if block[0] > xMax:
                    xMax = block[0]
                elif block[0] < xMin:
                    xMin = block[0]
                if block[1] > yMax:
                    yMax = block[1]
                elif block[1] < yMin:
                    yMin = block[1]
        if xMax >= self.grid.width:
            x = xMax - self.grid.width + 1
        elif xMin < 0:
            x = xMin
        else:
            x = 0
        if yMax >= self.grid.height:
            y = yMax - self.grid.height + 1
        elif yMin < 0:
            y = yMin
        else:
            y = 0
        return (x, y)


    def draw(self, screen):
        piece = self.center + self.blocks
        for block in piece:
            self.grid.drawBlock(screen, block[0], block[1], self.type)

class TetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10

        self.controller = TPieceControler()

        self.cells = []
        self.activePiece = TetrisPiece(self)
        self.controller.changePiece(self.activePiece)
        self.pieceQueue = Queue.Queue()

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.xOffset = (screenWidth - self.width * self.size) / 2
        self.yOffset = (screenHeight - self.height * self.size) / 2

    def realCoord(self, x, y):
        return (x * self.size + self.xOffset, y * self.size + self.yOffset)

    def placePiece(self):
        blocks = self.activePiece.coord()
        cellCol = self.activePiece.type
        topHeight = len(self.cells)

        for block in blocks:
            x, y = block
            
            if y >= topHeight:
                extraHeight = y - topHeight + 1
                topHeight += extraHeight
                for i in range(0, extraHeight):
                    self.cells.append(np.zeros(self.width, dtype = np.int))

            self.cells[y][x] = cellCol

        self.activePiece = TetrisPiece(self)
        self.controller.changePiece(self.activePiece)

        

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

    def update(self, gameTick = False):
        self.controller.recieveInput()
        if gameTick:
            self.activePiece.movePiece((0, -1))

    def draw(self, screen):
        self.drawBlocks(screen)
        self.activePiece.draw(screen)
        self.drawGrid(screen)

class Game(object):

    def draw(self, screen):
        screen.fill((200, 200, 200))
        self.grid.draw(screen)
        pygame.display.flip()

    def update(self, gameTick = False):
        self.grid.update(gameTick)
        
    def main(self, screen):
        self.grid = TetrisGrid(screen)
        gameSpeed = 15
        gameTick = gameSpeed

        while 1:
            clock = pygame.time.Clock()

            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.draw(screen)
            if gameTick == 0:
                self.update(True)
                gameTick = gameSpeed
            else:
                self.update()

            gameTick -= 1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
