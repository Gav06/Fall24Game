"""
Game Rewrite

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

import pygame
import scene

# Constant values (never change)
# Usually denoted in ALL CAPS
MAIN_MENU = scene.MainMenu()

width = 1280
height = 720
player_speed = 1
player = pygame.Rect(width // 2 - 20 // 2, height // 2 - 20 // 2, 20, 20)

screen = pygame.display.set_mode((width , height))
pygame.display.set_caption("")


running = True
while running:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            pygame.quit()
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

pygame.init()






pygame.quit()