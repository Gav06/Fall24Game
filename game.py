"""
Game Rewrite

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""
import pygame
pygame.init()

width = 1280
height = 720

black = (0,0,0)
white = (255, 255, 255)
font = pygame.font.Font(None, 100)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Shooter")


start_screen = "start"
game_screen = "game"
current_state =

running = True
while running:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:



pygame.quit()