from sys import exit
import pygame
import random
from math import floor, dist

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


class MoneyBox:
    def __init__(self):
        self.amount = 1000
        self.rect = pygame.Rect(0, 0, 300, 200)
    
    def draw(self):
        if self.amount > 0:
            color = "Green"
        else:
            color = "Red"

        moneyText = f"Money: $ {self.amount:.2f}"
        
        moneyBoxSurf = smallFont.render(moneyText, True, color)

        text_rect = moneyBoxSurf.get_rect(center=self.rect.center)
        screen.blit(moneyBoxSurf, text_rect)
    


class Bin:
    def __init__(self, position, color, multiplier):
        self.position = position
        self.color = color
        self.multiplier = multiplier
        self.rect = pygame.Rect(position[0], position[1], binWidth, binHeight)
        self.animateFrames = 0
        self.animateColor = "White"

    def animate(self):
        self.animateFrames = 10

    def update(self):
        if self.animateFrames:
            self.animateFrames -= 1

    def draw(self):
        if self.animateFrames:
            color = self.animateColor
            textColor = "Green"
        else:
            color = self.color
            textColor = (255, 255, 255)
        pygame.draw.rect(screen, color, self.rect, border_radius=corner_radius)
     
        if self.multiplier:  
            multiplierText = f"x{self.multiplier}"
        else:
            multiplierText = f"x{self.multiplier}"
        
        multiplier_surface = smallFont.render(multiplierText, True, textColor)
        text_rect = multiplier_surface.get_rect(center=self.rect.center)
        screen.blit(multiplier_surface, text_rect)

class Peg:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.animateFrames = 0
        self.animateColor = "White"

    
    def animate(self):
        self.animateFrames = 5

    def update(self):
        if self.animateFrames:
            self.animateFrames -= 1

    def draw(self):
        if self.animateFrames:
            color = self.animateColor
        else:
            color = self.color
        pygame.draw.circle(screen, color, self.position, pegRadius)

class Ball:
    def __init__(self, position):
        self.position = position
        self.color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        self.velocity = (random.randint(-3, 3), 0)
        self.acceleration = -9.8
        self.gravity = 0.075
        self.landedBin = None
        self.value = 1

    def update(self):
        self.velocity = (self.velocity[0], self.velocity[1] + 9.8 * self.gravity)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

        return self.position[1] > 710
            
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, ballRadius)

class ClickableArea:
    def __init__(self):
        self.size = (100, 50)
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
        self.money = 0
        self.clickableArea = ClickableArea()
        self.moneyBox = MoneyBox()
    

    def createBins(self):
        self.bins = []
        yPosition = 710

        for x in range(numBins):
           
            distCenter = floor(abs(x - (numBins - 1) / 2))
            gradientRatio = distCenter / ((numBins - 1) / 2)
            red = int(255 * gradientRatio)
            yellow = int(255 * (1 - gradientRatio))
            color = (red, yellow, 0)

            distCenterDict = {0: 0.3, 1: 0.5, 2: 1, 3: 2, 4: 5, 5: 10, 6: 50, 7: 250, 8: 1000, 9: 10000}

            if distCenter in distCenterDict:
                multiplier = distCenterDict[distCenter]
            else:
                multiplier = 10000
            
            bin_x_position = (
                screenLength / 2
                - spacing * numBins / 2
                - binWidth * numBins / 2
                + (spacing + binWidth) * x + spacing / 2
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
            self.moneyBox.amount -= 1

    def draw(self):
        self.clickableArea.draw()
        self.moneyBox.draw()

        for bin in self.bins:
            bin.update()
            bin.draw()

        for peg in self.pegs:
            peg.update()
            peg.draw()

        for _, ball in enumerate(self.balls):
            if ball.update():
                for bin in self.bins:
                    if ball.position[0] + ballRadius >= bin.position[0] and ball.position[0] - ballRadius <= bin.position[0] + binWidth:

                        self.moneyBox.amount += ball.value * bin.multiplier

                        bin.animate()

                        self.balls.remove(ball)

                        break

            else:
                for peg in self.pegs:
                    if dist(peg.position, ball.position) <= pegRadius + ballRadius:
                        # handle collisions:

                        peg.animate()

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