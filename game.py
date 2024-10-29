"""
Game Rewrite

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

import pygame
from pygame import Surface

import scene

# Sets with a default surface of a
class GameObject:
    # Uses a default surface which is just filled as white
    def __init__(self, rect):
        self.rect = rect
        self.surface = Surface((rect.w, rect.h))
        self.surface.fill((255, 255, 255))

    # "target" parameter is going to be the screen, or whatever surface we will blit onto
    def render(self, target):
        target.blit(self.surface, (self.rect.x, self.rect.y))

    # "events" parameter is the event list from the pygame loop
    def update(self, events):
        pass

# Constant values (never change)
# Usually denoted in ALL CAPS
MAIN_MENU = scene.MainMenu()

width = 1280
height = 720
player_speed = 1
player = pygame.Rect(width // 2 - 20 // 2, height // 2 - 20 // 2, 20, 20)

screen = pygame.display.set_mode((width , height))
clock = pygame.time.Clock()
pygame.display.set_caption("")


running = True
while running:
    for event in pygame.event.get():
<<<<<<< HEAD
        if pygame.event == pygame.QUIT:
            pygame.quit()
=======
        if event.type == pygame.QUIT:
            running = False
            break

>>>>>>> 6fd3a00b1e348f2b5bd01039d3194df9b303fdf7
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and player.top > 0:
        player.move_ip(0, -player_speed)
    if keys[pygame.K_s] and player.bottom < 720:
        player.move_ip(0, player_speed)
    if keys[pygame.K_a] and player.left > 0:
        player.move_ip(-player_speed, 0)
    if keys[pygame.K_d] and player.right < 1280:
        player.move_ip(player_speed, 0)

    screen.fill((0,0,0))
    pygame.draw.rect(screen,(255,255,255), player)
    pygame.display.flip()
    clock.tick(60)

pygame.init()






pygame.quit()