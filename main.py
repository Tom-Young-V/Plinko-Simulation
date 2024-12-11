from sys import exit
import pygame

pygame.init()

infoObject = pygame.display.Info()
screenLength = infoObject.current_w  # Screen width
screenHeight = infoObject.current_h - 200  # Screen height
screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("Plinko")
clock = pygame.time.Clock()
fontName = "New York Times"
font = pygame.font.SysFont(fontName, 40)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()
    clock.tick(60)


