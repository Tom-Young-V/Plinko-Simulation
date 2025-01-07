
binWidth = 15
binHeight = 15


class Bin:
    def __init__(self, position, color):
        # position: (x, y)
        self.position = position
        self.color = color
        # Create the rectangle using position and size
        self.rect = pygame.Rect(position[0], position[1], binWidth, binHeight)

    def draw(self, screen):
        # Draw the rectangle on the given screen
        pygame.draw.rect(screen, self.color, self.rect)