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

binWidth = 48
binHeight = 25
corner_radius = 5
spacing = 1
numBins = 20

pegRadius = 5
pegSpacingX = 50
pegSpacingY = 30

ballRadius = 8

smallFont = pygame.font.SysFont(fontName, 20)

class MoneyBox:
    def __init__(self):
        self.amount = 1000
        self.rect = pygame.Rect(0, 0, 300, 200)
    
    def draw(self):
        moneyText = f"Money: $ {self.amount:.2f}"
        moneyBoxSurf = smallFont.render(moneyText, True, "Green")
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
        
        multiplierText = f"x{self.multiplier}"
        multiplier_surface = smallFont.render(multiplierText, True, textColor)
        text_rect = multiplier_surface.get_rect(center=self.rect.center)
        screen.blit(multiplier_surface, text_rect)

class Peg:
    def __init__(self, position, color):
        self.position = pygame.Vector2(position)
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, pegRadius)


class Ball:
    def __init__(self, position):
        # 1. Initialize the ball's position using a 2D vector based on the input position.
        self.position = pygame.Vector2(position)

        # 2. Set the ball's color to a random RGB value with higher brightness (values between 128 and 255).
        self.color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

        # 3. Initialize the ball's velocity as a vector with a random horizontal speed (-2 to 2) and no vertical speed.
        self.velocity = pygame.Vector2(random.uniform(-2, 2), 0)

        # 4. Define the gravity factor that affects the ball's vertical acceleration.
        self.gravity = 0.1

        # 5. Define the damping factor that reduces velocity upon collision for realistic bounces.
        self.damping = 0.6

        # 6. Set the value property of the ball, possibly representing a score or type.
        self.value = 1

    def update(self):
        # 7. Apply gravity to the ball's vertical velocity.
        self.velocity.y += 9.8 * self.gravity

        # 8. Update the ball's position based on its velocity.
        self.position += self.velocity

        # 9. Check for collisions with pegs on the board.
        for peg in board.pegs:
            # 10. Calculate the distance between the ball and the current peg.
            distance = self.position.distance_to(peg.position)
            if distance < ballRadius + pegRadius:  # If they are overlapping:
                # 11. Calculate how much they overlap.
                overlap = ballRadius + pegRadius - distance

                # 12. Compute the normal vector for collision resolution.
                normal = (self.position - peg.position).normalize()

                # 13. Resolve overlap by moving the ball outward along the collision normal.
                self.position += normal * overlap

                # 14. Reflect the ball's velocity across the normal and apply damping to reduce its speed.
                self.velocity = self.velocity.reflect(normal) * self.damping

        # 15. Define triangular boundaries of the screen and check collisions with them.
        left_x = screenLength / 2 - pegSpacingX * 10
        right_x = screenLength / 2 + pegSpacingX * 10
        top_y = 100

        # 16. Check for collision with the left or right boundary.
        if self.position.x - ballRadius < left_x or self.position.x + ballRadius > right_x:
            # 17. Reverse horizontal velocity and apply damping.
            self.velocity.x = -self.velocity.x * self.damping

            # 18. Keep the ball inside the boundaries.
            self.position.x = max(left_x + ballRadius, min(self.position.x, right_x - ballRadius))

        # 19. Check for collision with the top boundary.
        if self.position.y - ballRadius < top_y:
            # 20. Reverse vertical velocity and apply damping.
            self.velocity.y = -self.velocity.y * self.damping

            # 21. Keep the ball below the top boundary.
            self.position.y = top_y + ballRadius

        # 22. Return True if the ball falls off the screen (below y=710).
        return self.position.y > 710

    def draw(self):
        # 23. Draw the ball as a circle on the screen with its color and position.
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), ballRadius)

class ClickableArea:
    def __init__(self):
        self.size = (30, 30)
        self.position = (screenLength / 2 - self.size[0] // 2, 90)
        self.color = (70, 74, 74)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def intersectMouse(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=corner_radius)

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

            distCenterDict = {0: 0.3, 1: 0.5, 2: 1, 3: 2, 4: 5, 5: 10, 6: 25, 7: 50, 8: 100, 9: 1000}
            multiplier = distCenterDict.get(distCenter, 10000)

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
            peg.draw()

        for ball in self.balls[:]:
            if ball.update():
                for bin in self.bins:
                    if bin.rect.collidepoint(ball.position):
                        self.moneyBox.amount += ball.value * bin.multiplier
                        bin.animate()
                        self.balls.remove(ball)
                        break

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
