"""
This is the main file for the pygame project for the Programming 1 Lecture class (Fall 2024)

Contributors (add your name to this list if you haven't):

Gavin Conley
Trevor Williams
Lucas Allen
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

font = pygame.font.Font(None, 74)

running = True


# Setup 5x5 game board
EMPTY = 0
CROSS = 1
RING = 2

board_5x5 = 5
board_size = board_5x5
current_board =
cell_size = 100
window_size = (cell_size * board_size, cell_size * board_size)

screen = pygame.display.set_mode(window_size)
pygame.display.set_mode("Not So Tic-Tac-Toe")



player = "X"

def game_loop(): # Game's main loop
    running = True
    while running:

        # Go through pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False


        pygame.display.flip()
        clock.tick(60)

def cpu_opponent():



game_loop()
pygame.quit()



