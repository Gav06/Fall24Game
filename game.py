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

white = (255, 255, 255)   # lines
dark_grey = (40, 40, 40)  # background
grey = (75, 75, 75)       # hover color
red = (255, 0, 0)         #  X's
green = (0, 255, 0)       #  O's

resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("Not-so-tic-tac-toe")
font = pygame.font.Font(None, 74)

# Setup 5x5 game board
EMPTY = 0
CROSS = 1 # default for player
RING = 2  # default for CPU

# We have a 5x5
board_size = 5

current_board = [[None for _ in range(board_size)] for _ in range(board_size)] # Had to look this one up

# this is the RECT board, not used for game logic, but used for rendering and other stuff instead.
# it starts off empty, we set it up later
rect_board = [[None for h in range(board_size)] for k in range(board_size)]

# the size horizontally or vertically (because it's a square) of each cell
cell_size = resolution[1] / board_size
# is the PLAYER winning? t/f, None if still undecided
winner = None
# self-explanatory
player_wins = 0
cpu_wins = 0

max_wins = 3

# this function is to set up the 2D array of Rects for rendering and stuff
def setup_board():
    for row in range(board_size):
        for col in range(board_size):
            rect_board[row][col] = pygame.Rect(cell_size * col, cell_size * row, cell_size, cell_size)

    pass

def draw_board(): #This is to draw out the 5x5 TicTacToe Board
    line_length = resolution[1]
    num_lines = board_size

    # draw horizontal lines
    for h in range(num_lines):
        if h == 0 or h == num_lines:
            continue
        n = cell_size * h

        pygame.draw.line(screen, white, (0, n), (line_length, n))
        pygame.draw.line(screen, white, (n, 0), (n, line_length))

"""
Board Layout:

(5 spaces, starts at 0, ends at 4, vertical and horizontal)

visual:

0 > 4
v   v
4 > 4,4
"""

# params: x coord of the mouse, y coord of the mouse
# returns: the row and column for the board array (numbers between 0 and 4)
def get_board_space(x, y):
    # check if the position given is out of bounds
    edge = resolution[1]

    if x <= 0 or x >= edge or y <= 0 or y >= edge:
        return None

    row = int(y // cell_size)

    col = int(x // cell_size)
    return (row, col)

def draw_plays():

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
    # rendering the outline
    draw_board()

    # get our mouse position
    mouse_pos = pygame.mouse.get_pos()
    # see what square that winds up in (if any) check to make sure this value is not None
    pos = get_board_space(mouse_pos[0], mouse_pos[1])

    # draw the overlay when mousing over a cell
    if pos is not None:
        r = rect_board[pos[0]][pos[1]]
        s = pygame.Surface((r.w - 1, r.h - 1))
        s.fill(grey)
        screen.blit(s, (r.x + 1, r.y + 1))

    # drawing the players' "Tics and tacs" lol
    draw_plays()




def update_pass():
    mouse_pos = pygame.mouse.get_pos()


def game_loop(): # Game's main loop
    running = True

    # fills our board array with all the rects
    setup_board()

    while running:
        """ update section (we update everything in the game BEFORE rendering) """
        # Go through pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        update_pass()

        """ render section (we can now render all of our changes) """
        screen.fill(dark_grey)
        render_pass()


        pygame.display.flip()
        clock.tick(60)

game_loop()
pygame.quit()


