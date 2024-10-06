"""
This is the main file for the pygame project for the Programming 1 Lecture class (Fall 2024)

Contributors (add your name to this list if you haven't):

Gavin Conley
Trevor Williams

"""
import pygame

pygame.init()

white = (255, 255, 255)   #lines
dark_grey = (90, 90, 90)  #background
red = (255, 0, 0)         #  X's
green = (0, 255, 0)       #  O's

resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
running = True


# Setup 5x5 game board
EMPTY = 0
CROSS = 1
RING = 2

board = [[EMPTY] * 5] * 5

def game_loop(): # Game's main loop
    running = True
    while running:

        # Go through pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)


pygame.quit()
game_loop()
#test comment
print("This is a git test") #comment



