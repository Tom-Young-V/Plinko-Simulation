from sys import exit
import pygame

pygame.init()

infoObject = pygame.display.Info()
screenLength = infoObject.current_w  # Screen width
screenHeight = infoObject.current_h - 120  # Screen height
screen = pygame.display.set_mode((screenLength, screenHeight))
pygame.display.set_caption("Plinko")
clock = pygame.time.Clock()
fontName = "Plinko"
font = pygame.font.SysFont(fontName, 40)


white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)
red = (255,0,0)
orange = (255,165,0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()
    clock.tick(60)






# Bins section

num_bins = 10
bin_width = screenLength // num_bins
bin_height = 15
bin_colors = []

for i in range(num_bins):
    if i < 2 or i >= 8:
        bin_colors.append(red)
    elif i == 2 or i == 3 or i == 7 or i == 8:
        bin_colors.append(orange)
    else:
        bin_colors.append(yellow)


for i in range(num_bins):
    pygame.draw.rect(
        screen,
        bin_colors[i],
        (i * bin_width, screenHeight - bin_height, bin_width, bin_height)
    )


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    pygame.display.flip()  

pygame.quit()
