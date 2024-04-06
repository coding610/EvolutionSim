import pygame
pygame.init()

from core import *
game = Core()


clock = pygame.time.Clock()
steps = 0
run = True
while run:
    clock.tick(game.tickspeed)
    game.fps = clock.get_fps()
    steps += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    game.update()
    if game.generation_time < steps:
        game.new_generation()
        steps = 0

    pygame.display.update()
