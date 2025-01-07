
from sys import exit
import pygame
import random

pygame.init()

displayObject = pygame.display.Info()
screenLength = displayObject.current_w  # Screen width
screenHeight = displayObject.current_h - 120  # Screen height
screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("Plinko")
clock = pygame.time.Clock()
fontName = "Plinko"
font = pygame.font.SysFont(fontName, 40)

binWidth = 40
binHeight = 25
corner_radius = 5
spacing = 10
numBins = 20

pegRadius = 5
pegSpacingX = 50
pegSpacingY = 30

ballRadius = 5
class Bin:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        #self.multiplier = multiplier
        self.rect = pygame.Rect(position[0], position[1], binWidth, binHeight)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=corner_radius)

class Peg:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, pegRadius)

class Ball:
    def __init__(self, position):
        self.position = position
        self.color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        self.velocity = (0, random.randint(-10, 10))
        self.acceleration = -9.8
        self.gravity = 0.1

    def update(self):
        self.velocity = (self.velocity[0], self.velocity[1] + 9.8 * self.gravity)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def draw(self):
        # self.update()
        pygame.draw.circle(screen, self.color, self.position, ballRadius)


class Board:
    def __init__(self):
        self.createBins()
        self.createPegs()
        
        self.balls = []

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

                maxPeg = 20 // 2 + abs(20 // 2 - 20)
                yColorDiff = y // 2
                xColorDiff = abs(y // 2 - x)
                red = 255
                blue = 255 - 250 * (xColorDiff + yColorDiff) / maxPeg
                green = 250 * (xColorDiff + yColorDiff) / maxPeg

                self.pegs.append(Peg((screenLength / 2 + pegSpacingX * (x - y / 2), 100 + y * pegSpacingY), (red, blue, green)))

    def addBall(self, position):
        self.balls.append(Ball(pygame.mouse.get_pos()))

    def draw(self):
        for bin in self.bins:
            bin.draw()

        for peg in self.pegs:
            peg.draw()

        for ball in self.balls:
            ball.draw()

board = Board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.addBall(pygame.mouse.get_pos())

    screen.fill((0, 0, 0)) 
    board.draw()
    
    pygame.display.update()
    clock.tick(60)






