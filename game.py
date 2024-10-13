"""
This is the main file for the pygame project for the Programming 1 Lecture class (Fall 2024)

Contributors (add your name to this list if you haven't):

Gavin Conley
Trevor Williams
Lucas Allen
"""
import random

import pygame

pygame.init()

white = (255, 255, 255)   #lines
dark_grey = (90, 90, 90)  #background
red = (255, 0, 0)         #  X's
green = (0, 255, 0)       #  O's

resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("Not-so-tic-tac-toe")
font = pygame.font.Font(None, 74)

# Setup 5x5 game board
EMPTY = 0
CROSS = 1
RING = 2

width, height = 1000
board_5x5 = 5
board_size = board_5x5
current_board = [[None for _ in range(board_size)] for _ in range(board_size)] # Had to look this one up
cell_size = 100
window_size = (width, height)



player = "X"
winner = None
player_wins = 0
cpu_wins = 0
max_wins = 3

def board_drawing(): #This is to draw out the 5x5 TicTacToe Board

    pass


def game_winner(): #I'm going to call this function under CPU Opponent -Trevor
    pass

"""
def cpu_opponent():
    global player
    moves = [(row, column) for row in range(board_size) for column in range(board_size) if not current_board[row][column]]
    if moves:
        row = random.choice(moves)
        column = random.choice(moves)
        current_board[row][column] = "O"
"""
def render_pass():
    pass

def update_pass():
    pass


def game_loop(): # Game's main loop
    running = True
    while running:
        """ update section (we update everything in the game BEFORE rendering """
        # Go through pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        """ render section (we can now render all of our changes) """
        screen.fill(dark_grey)

        pygame.display.flip()
        clock.tick(60)

game_loop()
pygame.quit()



