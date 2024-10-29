"""
This is the main file for the pygame project for the Programming 1 Lecture class (Fall 2024)

Contributors (add your name to this list if you haven't):

Gavin Conley
Trevor Williams
Lucas Allen
"""
import random
import pygame

white = (255, 255, 255)   # lines
dark_grey = (40, 40, 40)  # background
grey = (75, 75, 75)       # hover color
red = (255, 0, 0)         #  X's
green = (0, 255, 0)       #  O's

pygame.init()
pygame.font.init()#initializes font so we can display the score

resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("Not-so-tic-tac-toe")
font = pygame.font.Font(None, 28)

# Setup 5x5 game board
EMPTY = 0

@@ -32,7 +32,8 @@ RING = 2  # default for CPU
# We have a 5x5
board_size = 5


# This is the 2d array that stores if each cell is an X, O, or nothing.
game_board = [[EMPTY for i in range(board_size)] for j in range(board_size)] # Had to look this one up

# this is the RECT board, not used for game logic, but used for rendering and other stuff instead.
# it starts off empty, we set it up later

@@ -40,12 +41,13 @@ rect_board = [[None for h in range(board_size)] for k in range(board_size)]

# the size horizontally or vertically (because it's a square) of each cell
cell_size = resolution[1] / board_size

# is the PLAYER winning? t/f, None if still undecided
winner = None

# self-explanatory
player_wins = 0
cpu_wins = 0
max_wins = 3

# this function is to set up the 2D array of Rects for rendering and stuff


@@ -96,13 +98,41 @@ def get_board_space(x, y):
    return (row, col)

def draw_plays():
    for row in range(board_size):
        for col in range(board_size):
            cell_state = game_board[row][col]

            if cell_state != CROSS:
                continue

            text = font.render("x", True, white)
            cell_rect = rect_board[row][col]
            screen.blit(text, (cell_rect.centerx, cell_rect.centery))
    pass


def game_winner(): #I'm going to call this function under CPU Opponent -Trevor
    pass

# called when mouse is pressed
def handle_mouse(x, y):
    target_space = get_board_space(x, y)

    if target_space is None:
        return


    row = target_space[0]
    col = target_space[1]

    cell = game_board[row][col]

    if cell == EMPTY:
        game_board[row][col] = CROSS
    elif cell == CROSS:
        game_board[row][col] = EMPTY


"""
def cpu_opponent():
    global player

@@ -110,8 +140,9 @@ def cpu_opponent():
    if moves:
        row = random.choice(moves)
        column = random.choice(moves)
        current_board[row][column] = 
"""

def render_pass():
    # rendering the outline
    draw_board()

@@ -131,27 +162,39 @@ def render_pass():
    # drawing the players' "Tics and tacs" lol
    draw_plays()

    # Draw the text
    text_x = resolution[1] + 2
    title = font.render("5x5 Tic-Tac-Toe", True, white)
    p_score = font.render(f"Player score: {player_wins}", True, white)
    cpu_score = font.render(f"CPU score: {cpu_wins}", True, white)

    screen.blit(title, (text_x, 10))
    screen.blit(p_score, (text_x, 30))
    screen.blit(cpu_score, (text_x, 50))



def update_pass(events):
    # check for mouse click
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse(event.pos[0], event.pos[1])

    pass


def game_loop(): # Game's main loop
    running = True


    while running:
        """ update section (we update everything in the game BEFORE rendering) """
        # Go through pygame events
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False


        update_pass(events)

        """ render section (we can now render all of our changes) """
        screen.fill(dark_grey)

@@ -161,7 +204,17 @@ def game_loop(): # Game's main loop
        pygame.display.flip()
        clock.tick(60)

# main function
def __main__():
    # initialize
    setup_board()

    # loop
    game_loop()

    # exit
    pygame.quit()


if __name__ == "__main__":
    __main__()