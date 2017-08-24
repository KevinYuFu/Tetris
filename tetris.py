import pygame
import numpy as np

Black = (0, 0, 0)

Colour = { 0 : (150, 150, 150),
           1 : (0, 150, 150),
           2 : (150, 150, 0),
           3 : (150, 0, 0),
           4 : (0, 150, 0),
           5 : (200, 130, 0),
           6 : (0, 0, 150),
           7 : (150, 0, 150) }
Empty = (150, 150, 150)

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


class tetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10
        self.cells = []

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
        self.drawGrid(screen)

class Game(object):
    #def __init__(self):

    def draw(self, screen):
        screen.fill((200, 200, 200))
        self.grid.draw(screen)
        pygame.display.flip()
        
    def main(self, screen):
        self.grid = tetrisGrid(screen)

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
