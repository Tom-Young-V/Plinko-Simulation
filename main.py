from sys import exit
import pygame
import random
from math import floor

pygame.init()

displayObject = pygame.display.Info()
screenLength = displayObject.current_w  # Screen width
screenHeight = displayObject.current_h - 100  # Screen height
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

smallFont = pygame.font.SysFont(fontName, 20)

class Bin:
    def __init__(self, position, color, multiplier):
        self.position = position
        self.color = color
        self.multiplier = multiplier
        self.rect = pygame.Rect(position[0], position[1], binWidth, binHeight)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=corner_radius)
     
        if self.multiplier:  
            multiplierText = f"x{int(self.multiplier)}"
        else:
            multiplierText = f"x{self.multiplier:.1f}"  

       
        multiplier_surface = smallFont.render(multiplierText, True, (255, 255, 255))
        text_rect = multiplier_surface.get_rect(center=self.rect.center)
        screen.blit(multiplier_surface, text_rect)


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
        self.velocity = (random.randint(-3, 3), 0)
        self.acceleration = -9.8
        self.gravity = 0.1

    def update(self):
        self.velocity = (self.velocity[0], self.velocity[1] + 9.8 * self.gravity)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def draw(self):
        self.update()
        pygame.draw.circle(screen, self.color, self.position, ballRadius)


class ClickableArea:
    def __init__(self):
        self.size = (200, 50)
        self.position = (screenLength / 2 - self.size[0] // 2, 50)
        self.color = (70, 74, 74)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def intersectMouse(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius = corner_radius)

class Board:
    def __init__(self):
        self.createBins()
        self.createPegs()
        self.balls = []

        self.clickableArea = ClickableArea()

    def createBins(self):
        self.bins = []
        yPosition = screenHeight - 150

        for x in range(numBins):
           
            distCenter = floor(abs(x - (numBins - 1) / 2))
            gradientRatio = distCenter / ((numBins - 1) / 2)
            red = int(255 * gradientRatio)
            yellow = int(255 * (1 - gradientRatio))
            color = (red, yellow, 0)

            distCenterDict = {0: 0.3, 1: 0.5, 2: 1, 3: 2, 4: 5, 5: 10}

            if distCenter in distCenterDict:
                multiplier = distCenterDict[distCenter]
            else:
                multiplier = 50
            
            bin_x_position = (
                screenLength / 2
                - spacing * numBins / 2
                - binWidth * numBins / 2
                + (spacing + binWidth) * x
            )
            self.bins.append(Bin((bin_x_position, yPosition), color, multiplier))
    
    def createPegs(self):
        self.pegs = []
            
        for y in range(20):
            for x in range(y + 1):
                if not y:
                    continue


                maxPeg = 20 // 2 + abs(20 // 2 - 20)
                yColorDiff = y // 2
                xColorDiff = abs(y // 2 - x)
                red = 255
                blue = 255 - 250 * (xColorDiff + yColorDiff) / maxPeg
                green = 250 * (xColorDiff + yColorDiff) / maxPeg

                self.pegs.append(Peg((screenLength / 2 + pegSpacingX * (x - y / 2), 100 + y * pegSpacingY), (red, blue, green)))

    def addBall(self, position):
        if self.clickableArea.intersectMouse():
            self.balls.append(Ball(pygame.mouse.get_pos()))

    def draw(self):
        self.clickableArea.draw()

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

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is held down
                board.addBall(pygame.mouse.get_pos())

    screen.fill((0, 0, 0)) 
    board.draw()
    
    pygame.display.update()
    clock.tick(60)