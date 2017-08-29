import pygame
import math
from collections import deque
from random import randint
import numpy as np

Black = (0, 0, 0)

Colour = { 0 : (200, 200, 200), # None
           1 : (0, 200, 200),   # I
           2 : (200, 200, 0),   # O
           3 : (200, 0, 0),     # Z
           4 : (0, 200, 0),     # S
           5 : (250, 160, 0),   # L
           6 : (0, 0, 200),     # J
           7 : (200, 0, 200),   # T

           8 : (100, 150, 150),   # I Ghost
           9 : (150, 150, 100),   # O Ghost
           10 : (150, 100, 100),    # Z Ghost
           11 : (100, 150, 100),    # S Ghost
           12 : (200, 130, 100),  # L Ghost
           13 : (100, 100, 150),    # J Ghost
           14 : (150, 100, 150) } # T Ghost

TPieceCoord = { 1 : ((-1, 0), (0, 0), (1, 0), (2, 0)),      # I
                2 : ((0, -1), (1, -1), (0, 0), (1, 0)),     # O
                3 : ((-1, 0), (0, 0), (0, -1), (1, -1)),    # Z
                4 : ((-1, -1), (0, -1), (0, 0), (1, 0)),    # S
                5 : ((-1, 0), (0, 0), (1, 0), (1, 1)),      # L
                6 : ((-1, 1), (-1, 0), (0, 0), (1, 0)),     # J
                7 : ((-1, 0), (0, 0), (1, 0), (0, -1)) }    # T

TPieceFrameCoord = { 1 : TPieceCoord[1] + np.array((1, 1.5)),     # I
                     2 : TPieceCoord[2] + np.array((1, 2)),       # O
                     3 : TPieceCoord[3] + np.array((1.5, 2)),     # Z
                     4 : TPieceCoord[4] + np.array((1.5, 2)),     # S
                     5 : TPieceCoord[5] + np.array((1.5, 1)),     # L
                     6 : TPieceCoord[6] + np.array((1.5, 1)),     # J
                     7 : TPieceCoord[7] + np.array((1.5, 2)) }    # T

class TPieceControler():
    def __init__(self, grid, tPiece = None):
        self.leftHeld = False
        self.rightHeld = False
        self.upHeld = False
        self.downHeld = False
        self.spaceHeld = False
        self.cHeld = False
        self.grid = grid
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
            else:
                self.downHeld = False

            if key[pygame.K_SPACE]:
                if self.spaceHeld == False:
                    self.tPiece.center = self.tPiece.ghostCenter
                    self.tPiece.grid.placePiece()
                    self.spaceHeld = True
            else:
                self.spaceHeld = False

            if key[pygame.K_c]:
                self.grid.swapHold()

class TetrisPiece():
    def __init__(self, grid, pType = None):
        if pType is None:
            self.type = randint(1, 7)
        else:
            self.type = pType
        self.grid = grid

        beginningHeight = grid.height - 1
        gridCenter = int(math.floor(grid.width/2))
        if self.type in (5, 6):
            beginningHeight -= 1
        self.center = np.array([gridCenter, beginningHeight])

        self.blocks = np.asarray(TPieceCoord[self.type])
        self.ghostCenter = self.calcGhostPiece()

        self.readyToPlace = False

    def calcGhostPiece(self):
        x, y = self.center
        while 1:
            tempGhost = self.blocks + (x, y)
            for block in tempGhost:
                if self.grid.blockOverlap(block):
                    return (x, y + 1)
            y -= 1
        
    def movePiece(self, direction):
        height = self.grid.height
        width = self.grid.width

        tempCenter = self.center + direction

        fix = self.enclose(tempCenter)
        tempBlocks = tempCenter + self.blocks

        validPosition = True
        if fix == (0, 0):
            for block in tempBlocks:
                if  self.grid.blockOverlap(block):
                    validPosition = False
                    break
        else:
            validPosition = False

        if validPosition:
            self.center = tempCenter
            self.ghostCenter = self.calcGhostPiece()
        elif direction == (0, -1):
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
        self.ghostCenter = self.calcGhostPiece()
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
        ghostPiece = self.ghostCenter + self.blocks

        for block in ghostPiece:
            self.grid.drawBlock(screen, block[0], block[1], self.type + 7)

        for block in piece:
            self.grid.drawBlock(screen, block[0], block[1], self.type)

class TetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10
        self.cells = []

        self.controller = TPieceControler(self)

        self.heldPiece = None
        self.pieceQueue = deque()
        for i in range(5):
            self.pieceQueue.append(randint(1, 7))
        self.nextPiece()

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.xOffset = (screenWidth - self.width * self.size) / 2
        self.yOffset = (screenHeight - self.height * self.size) / 2

    def nextPiece(self):
        self.activePiece = TetrisPiece(self, self.pieceQueue.popleft())
        self.pieceQueue.append(randint(1, 7))
        self.controller.changePiece(self.activePiece)

    def swapHold(self):
        self.activePiece, self.heldPiece = TetrisPiece(self, self.heldPiece), self.activePiece.type
        if self.activePiece is None:
            self.activePiece = self.nextPiece()
        else:
            self.controller.changePiece(self.activePiece) # This is a smell

    def placePiece(self):
        blocks = self.activePiece.center + self.activePiece.blocks
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

        self.clearFullRows()

        #self.activePiece = TetrisPiece(self)
        #self.controller.changePiece(self.activePiece)
        self.nextPiece()

    def clearFullRows(self):
        y = 0
        topHeight = len(self.cells)
        while y < topHeight:
            delete = True
            for n in self.cells[y]:
                if n == 0:
                    delete = False
                    break

            if delete:
               del self.cells[y] 
               topHeight -= 1
            else:
                y += 1

    def blockOverlap(self, block):
        topHeight = len(self.cells)
        x, y = block
        if y < 0:
            return True
        if y < topHeight and self.cells[y][x] != 0:
            return True
        return False

    def update(self, gameTick = False):
        self.controller.recieveInput()
        if gameTick:
            self.activePiece.movePiece((0, -1))

    def realCoord(self, x, y):
        return (x * self.size + self.xOffset, y * self.size + self.yOffset)

    def drawGrid(self, screen):
        # Main Grid
        for y in range(0, self.height + 1):
            pygame.draw.line(screen, Black, self.realCoord(0, y), self.realCoord(self.width, y))
        for x in range(0, self.width + 1):
            pygame.draw.line(screen, Black, self.realCoord(x, 0), self.realCoord(x, self.height))

        # Held Frame
        frameSize = 4 * self.size
        heldFrame = pygame.rect.Rect(self.realCoord(-5, 0), (frameSize, frameSize))
        pygame.draw.rect(screen, Black, heldFrame, 1)

        # Queue Frame
        for i in range(5):
            queueFrame = pygame.rect.Rect(self.realCoord(self.width + 1, 4 * i), (frameSize, frameSize))
            pygame.draw.rect(screen, Black, queueFrame, 1)

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

    def drawFramePiece(self, screen, leftCorner, pType):
        framePiece = TPieceFrameCoord[pType] + leftCorner
        for block in framePiece:
            x, y = block
            blockRect = pygame.rect.Rect(self.realCoord(x, y), (self.size, self.size))
            pygame.draw.rect(screen, Colour[pType], blockRect, 0)
            pygame.draw.rect(screen, Black, blockRect, 1)

    def drawQueuedPieces(self, screen):
        # Draw Held Piece
        if self.heldPiece is not None:
            self.drawFramePiece(screen, (-5, 0), self.heldPiece)

        # Draw Queue
        for i, pType in enumerate(self.pieceQueue):
            self.drawFramePiece(screen, (self.width + 1, 4 * i), pType)

    def draw(self, screen):
        self.drawBlocks(screen)
        self.activePiece.draw(screen)

        self.drawQueuedPieces(screen)

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
