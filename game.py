"""
Game Rewrite

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

import pygame

width = 1280
height = 720



screen = pygame.display.set_mode(width , height)
pygame.display.set_caption("")


running = True
while running:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            pygame.quit()

pygame.init()

pygame.quit()