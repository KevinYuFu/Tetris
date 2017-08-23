import pygame

Black = (0, 0, 0)

class tetrisGrid():
    def __init__(self, screen):
        self.size = 20
        self.height = 20
        self.width = 10

        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        self.xOffset = (screenWidth - self.width * self.size) / 2
        self.yOffset = (screenHeight - self.height * self.size) / 2

    def draw(self, screen):
        for y in range(0, self.height + 1):
            yLoc = y * self.size + self.yOffset
            pygame.draw.line(screen, Black, (self.xOffset, yLoc), (self.xOffset + self.width * self.size, yLoc))
        for x in range(0, self.width + 1):
            xLoc = x * self.size + self.xOffset
            pygame.draw.line(screen, Black, (xLoc, self.yOffset), (xLoc, self.yOffset + self.height * self.size))

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
