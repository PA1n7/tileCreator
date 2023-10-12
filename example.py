import tiler
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

background = tiler.tiledMap(screen, "example_conf.txt", "example_defs.json")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((255, 0, 0))
    background.draw()
    pygame.display.update()