from sys import exit
import pygame

pygame.init()

displayObject = pygame.display.Info()
screenLength = displayObject.current_w  # Screen width
screenHeight = displayObject.current_h - 120  # Screen height
screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("Plinko")
clock = pygame.time.Clock()
fontName = "Plinko"
font = pygame.font.SysFont(fontName, 40)


binWidth = 100
binHeight = 25
corner_radius = 5
spacing = 10
numBins = 10

pegRadius = 5
pegSpacingX = 50
pegSpacingY = 30

class Bin:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], binWidth, binHeight)

    def draw(self):
        # Draw the rectangle on the given screen
        pygame.draw.rect(screen, self.color, self.rect, border_radius=corner_radius)

class Peg:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self):
        # Draw the circle (peg) on the screen
        pygame.draw.circle(screen, self.color, self.position, pegRadius)


class Board:
    def __init__(self):
        self.createBins()
        self.createPegs()

    def createBins(self):
        self.bins = []

        yPosition = screenHeight - 150

        for x in range(numBins):
            dcenter = abs(x - (numBins - 1)/2)
            gradientRatio = dcenter / ((numBins - 1) / 2)
            red = int(255 * gradientRatio)
            yellow = int(255 *(1-gradientRatio))
            color = (red,yellow,0)
            self.bins.append(Bin((screenLength / 2 - spacing * numBins / 2 - binWidth * numBins / 2 + (spacing + binWidth) * x, yPosition), color))

    def createPegs(self):
        self.pegs = []
            

        for y in range(20):
            for x in range(y + 1):
                
                # Gradient color based on position
                red = int(255 * (x / (y + 1))) % 256
                blue = int(255 * (y / 20)) % 256
                green = 255 - red  # Inverse of red for contrast

                print(x, y, screenLength / 2, screenLength / 2 + 50 * (x - y / 2))
                self.pegs.append(Peg((screenLength / 2 + pegSpacingX * (x - y / 2), 100 + y * pegSpacingY), (red, blue, green)))

    def draw(self):
        for bin in self.bins:
            bin.draw()

        for peg in self.pegs:
            peg.draw()

board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0)) 
    board.draw()
        
    pygame.display.update()
    clock.tick(60)






