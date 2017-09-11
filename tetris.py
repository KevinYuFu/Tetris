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

# Class managing User Input to comunicate with the Grid and Active Piece
class TPieceControler():
    def __init__(self, game, tPiece = None):
        self.leftHeld = False
        self.rightHeld = False
        self.upHeld = False
        self.downHeld = False
        self.spaceHeld = False
        self.cHeld = False
        self.swap = False

        self.heldCounter = 3
        self.heldSpeed = 2
        self.leftHeldCount = self.heldCounter
        self.rightHeldCount = self.heldCounter

        self.game = game
        self.tPiece = tPiece

    # Change activePiece to control
    def changePiece(self,tPiece):
        self.tPiece = tPiece
        self.swap = False

    # Perform tasks based on user input
    def recieveInput(self):
        if self.tPiece is not None:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_h]:
                if self.leftHeld == False:
                    self.tPiece.movePiece((-1, 0))
                    self.leftHeld = True
                elif self.leftHeldCount == 0:
                    self.tPiece.movePiece((-1, 0))
                    self.leftHeldCount = self.heldSpeed
                else:
                    self.leftHeldCount -= 1
            else:
                self.leftHeld = False
                self.leftHeldCount = self.heldCounter

            if key[pygame.K_RIGHT] or key[pygame.K_l]:
                if self.rightHeld == False:
                    self.tPiece.movePiece((1, 0))
                    self.rightHeld = True
                elif self.rightHeldCount == 0:
                    self.tPiece.movePiece((1, 0))
                    self.rightHeldCount = self.heldSpeed
                else:
                    self.rightHeldCount -= 1
            else:
                self.rightHeld = False
                self.rightHeldCount = self.heldCounter

            if key[pygame.K_UP] or key[pygame.K_k]:
                if self.upHeld == False:
                    self.tPiece.rotate()
                    self.upHeld = True
            else:
                self.upHeld = False

            if key[pygame.K_DOWN] or key[pygame.K_j]:
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
                    self.game.placePiece()
                    self.spaceHeld = True
            else:
                self.spaceHeld = False

            if key[pygame.K_c]:
                if self.swap == False:
                    self.game.swapHold()
                    self.swap = True


# Class representing an active Tetris Piece
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

    # Calculate coordinate for a ghost visualization of the piece at the lowest y co-ordinate
    def calcGhostPiece(self):
        x, y = self.center
        while 1:
            tempGhost = self.blocks + (x, y)
            if not self.grid.validPieceLocation(tempGhost):
                return (x, y + 1)
            y -= 1

    # Move the active piece by the given direction
    # direction is a 2d-tuple representing how much to move in x and y
    # Returns True when piece successfully moved. Otherwise returns False
    def movePiece(self, direction):
        tempCenter = self.center + direction
        if self.grid.validPieceLocation(tempCenter + self.blocks):
            self.center = tempCenter
            self.ghostCenter = self.calcGhostPiece()
            return True
        else:
            return False

    # Rotates active piece
    def rotate(self):
        if self.type == 2: return
        #tempBlocks = np.array([np.array(y, -x) for x, y in self.blocks])
        tempBlocks = np.array(self.blocks)
        for i in range(0, 4):
            x, y = tempBlocks[i]
            tempBlocks[i] = np.array([y, -x])

        fix = self.grid.fitRotatedPiece(self.center + tempBlocks)
        if fix:
            self.center += fix
            self.blocks = tempBlocks
            self.ghostCenter = self.calcGhostPiece()


    # Draw the Active piece and it's ghost image
    def draw(self, screen):
        piece = self.center + self.blocks
        ghostPiece = self.ghostCenter + self.blocks

        for block in ghostPiece:
            self.grid.drawBlock(screen, block[0], block[1], self.type + 7)

        for block in piece:
            self.grid.drawBlock(screen, block[0], block[1], self.type)

# Class representing the grid which Tetris is played on
class TetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10
        self.cells = []

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.xOffset = (screenWidth - self.width * self.size) / 2
        self.yOffset = (screenHeight - self.height * self.size) / 2

    # Store the piece coordinates into the grid and remove any complete rows
    def placePiece(self, blocks, col):
        topHeight = len(self.cells)

        for block in blocks:
            x, y = block
            
            if y >= topHeight:
                extraHeight = y - topHeight + 1
                topHeight += extraHeight
                for i in range(0, extraHeight):
                    self.cells.append(np.zeros(self.width, dtype = np.int))

            self.cells[y][x] = col 

        self.clearCompleteRows()

    # Check for filled rows and clears them
    def clearCompleteRows(self):
        y = 0
        topHeight = len(self.cells)
        while y < topHeight:
            delete = True
            for n in self.cells[y]:
                if n == 0:
                    y += 1
                    break
            else:
                del self.cells[y] 
                topHeight -= 1

    # Check if coordinates are out of bound
    # returns coordinates representing the offset
    def outOfRange(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    # Check if a piece fits on the grid
    def validPieceLocation(self, blocks):
        topHeight = len(self.cells)
        for block in blocks:
            x, y = block
            if self.outOfRange(x, y):
                return False
            if y < topHeight and self.cells[y][x] != 0:
                return False
        return True

    # Search for fix on piece position after a rotation
    def fitRotatedPiece(self, piece):
        for i in range(3):
            for j in range(2):
                if j: w = i
                else: w = -i
                for h in range(2):
                    if self.validPieceLocation(piece + np.asarray((w, h))):
                        return (w, h)
        print("Failed to Rotate")
        return False

    # Calculates the screen pixel coordinate of a grid x, y coordinate
    def realCoord(self, x, y):
        return (x * self.size + self.xOffset, y * self.size + self.yOffset)

    # Draw the grid
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

    # Draw blocks in the grid
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

    # Draws a single block given coordinates:
    # x, h are the cordinates of the block in the grid
    # col represents the colour of the block
    def drawBlock(self, screen, x, h, col):
        y = self.height - h - 1
        block = pygame.rect.Rect(self.realCoord(x, y),(self.size, self.size))
        pygame.draw.rect(screen, Colour[col], block, 0)
        pygame.draw.rect(screen, Black, block, 1)

    # Draw a piece that is displayed in one of the "picture frames"
    # A picture frame displays either the held piece or the queued pieces
    def drawFramePiece(self, screen, leftCorner, pType):
        framePiece = TPieceFrameCoord[pType] + leftCorner
        for block in framePiece:
            x, y = block
            self.drawBlock(screen, x, y, pType)

    # Draw the pieces in the picture frames: Held
    def drawHeldPiece(self, screen, heldPiece):
        frameTop = self.height - 4
        # Draw Held Piece
        if heldPiece is not None:
            self.drawFramePiece(screen, (-5, frameTop), heldPiece)

    # Draw the pieces in the picture frames: Queued pieces
    def drawQueuedPieces(self, screen, pieceQueue):
        frameTop = self.height - 4
        # Draw Queue
        for i, pType in enumerate(pieceQueue):
            self.drawFramePiece(screen, (self.width + 1, frameTop - 4 * i), pType)

    # Draw contents of the grid
    def draw(self, screen):
        self.drawBlocks(screen)
        self.drawGrid(screen)

# Class representing the tetris game
class Game(object):
    def draw(self, screen):
        screen.fill((200, 200, 200))
        self.grid.drawHeldPiece(screen, self.heldPiece)
        self.grid.drawQueuedPieces(screen, self.pieceQueue)
        self.grid.draw(screen)
        self.activePiece.draw(screen)
        pygame.display.flip()

    # update the state of the game
    def update(self):
        self.controller.recieveInput()
        if self.gameTick == 0:
            if not self.activePiece.movePiece((0, -1)):
                self.placePiece()
            self.gameTick = self.gameSpeed


    # Pop of the next Queued piece and add to the Queue
    def nextPiece(self):
        self.activePiece = TetrisPiece(self.grid, self.pieceQueue.popleft())
        self.pieceQueue.append(randint(1, 7))
        self.controller.changePiece(self.activePiece)

    # Switch the active piece with the held piece
    def swapHold(self):
        if self.heldPiece is None:
            self.heldPiece = self.activePiece.type
            self.nextPiece()
            self.controller.changePiece(self.activePiece) # This is a smell
        else:
            self.activePiece, self.heldPiece = TetrisPiece(self.grid, self.heldPiece), self.activePiece.type
            self.controller.changePiece(self.activePiece) # This is a smell

    # Send active piece data to the grid to be stored and prepare the next piece
    def placePiece(self):
        blocks = self.activePiece.center + self.activePiece.blocks
        cellCol = self.activePiece.type

        self.grid.placePiece(blocks, cellCol)

        self.nextPiece()

    # Main function that executes the game
    def main(self, screen):
        # Setup grid and controler object
        self.grid = TetrisGrid(screen)
        self.controller = TPieceControler(self)

        self.heldPiece = None
        self.pieceQueue = deque()
        for i in range(5):
            self.pieceQueue.append(randint(1, 7))
        self.nextPiece()

        self.gameSpeed = 15
        self.gameTick = self.gameSpeed
        self.readyToPlace = False

        while 1:
            clock = pygame.time.Clock()

            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.draw(screen)
            self.update()
            self.gameTick -= 1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
