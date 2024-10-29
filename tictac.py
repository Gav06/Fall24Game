"""
This is the main file for the pygame project for the Programming 1 Lecture class (Fall 2024)

Contributors (add your name to this list if you haven't):

Gavin Conley
Trevor Williams
Lucas Allen
"""

import pygame

"""
Color constants
"""
white = (255, 255, 255)   # lines
dark_grey = (40, 40, 40)  # background
grey = (75, 75, 75)       # hover color
red = (255, 0, 0)         #  X's
green = (0, 255, 0)       #  O's

"""
Pygame constant values
"""
pygame.init()
resolution = (640, 480)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("Not-so-tic-tac-toe")
font = pygame.font.Font(None, 28)

"""
Integer constant values for determining who placed what on the board,
and defining the board
"""
EMPTY = 0 # empty cell (blank)
PLAYER = 1 # default for player (CROSS)
CPU = 2  # default for CPU (RING)
board_size = 5
# This is the 2d array that stores if each cell is an X, O, or nothing.
game_board = [[EMPTY for i in range(board_size)] for j in range(board_size)] # Had to look this one up
# this is the RECT board, not used for game logic, but used for rendering and other stuff instead.
# it starts off empty, we set it up later
rect_board = [[None for h in range(board_size)] for k in range(board_size)]
# the size horizontally or vertically (because it's a square) of each cell
cell_size = resolution[1] / board_size

"""
Boolean value for if the player wins,
True if player win
False if cpu win
None if game is still ongoing
"""
winner = None
# Player starts first on the first level
current_turn = PLAYER

"""
Keeping track of scores
"""
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


def draw_hover_square():
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

"""
Board Layout:

(5 spaces, starts at 0, ends at 4, vertical and horizontal)

visual:

0 ----- 4
|       |
|       |
4 ----- 4,4

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
    for row in range(board_size):
        for col in range(board_size):
            cell_state = game_board[row][col]
            cell_rect = rect_board[row][col]

            if cell_state == PLAYER:
                text = font.render("x", True, red)
            elif cell_state == CPU:
                text = font.render("o", True, green)
            else:
                continue

            text_rect = text.get_rect(center=cell_rect.center)
            screen.blit(text, text_rect)


def game_winner(): #I'm going to call this function under CPU Opponent -Trevor
    #Row check for  winner
    for row in range(board_size):
        if game_board[row][0] != EMPTY and all(game_board[row][col] == game_board[row][0]for col in range(board_size)):
            return game_board[row][0]
    #Column check for winner
    for col in range(board_size):
        if game_board[col][0] != EMPTY and all(game_board[row][col] == game_board[row][0] for row in range(board_size)):
            return game_board[0][col]
    #Diagnol Check
    if game_board[0][0] != EMPTY and all(game_board[i][i] == game_board[0][0] for i in range(board_size)):
        return game_board[0][0]
    if game_board[0][board_size - 1] != EMPTY and all(game_board[i][board_size - 1 - i] == game_board[0][board_size - 1] for i in range(board_size)):
        return game_board[0][board_size - 1]
    #Tie Check
    if all(game_board[row][col] != EMPTY for row in range(board_size) for col in range(board_size)):
        return "tie game"

    return None

# checking the board each time a cell is placed
def board_evaluation():
    winner = game_winner()

    if winner == PLAYER:
        return -10
    elif winner == CPU:
        return 10
    elif winner == "tie game":
        return 0

    return None


def minimax(depth, minimaxing):
    score = board_evaluation()

    if score is not None:
        return score

    if minimaxing:
        best_score = -float("inf")
        for row in range(board_size):
            for col in range(board_size):
                if game_board[row][col] == EMPTY:
                    game_board[row][col] = CPU
                    score = minimax(depth + 1, False)
                    game_board[row][col] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(board_size):
            for col in range(board_size):
                if game_board[row][col] == EMPTY:
                    game_board[row][col] = PLAYER
                    score = minimax(depth + 1, True)
                    game_board[row][col] = EMPTY
                    best_score = min(score, best_score)
        return best_score


def cpu_opponent():
    best_score = -float('inf')
    best_move = None

    for row in range(board_size):
        for col in range(board_size):
            if game_board[row][col] == EMPTY:
                game_board[row][col] = CPU
                score = minimax(0, False)
                game_board[row][col] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move is not None:
        game_board[best_move[0]][best_move[1]] = CPU

# handle mouse input when the mouse is clicked (user input)
def handle_player_input(x, y):
    global current_turn

    if current_turn != PLAYER:
        return
    else:
        current_turn = CPU

    target_space = get_board_space(x, y)

    if target_space is None:
        return


    row = target_space[0]
    col = target_space[1]

    cell = game_board[row][col]

    if cell == EMPTY:
        game_board[row][col] = PLAYER
    elif cell == PLAYER:
        game_board[row][col] = EMPTY

# This gets called when it is the CPU's turn
def handle_cpu_input():
    pass

# rendering logic for each frame
def render_pass():
    # rendering the outline
    draw_board()
    draw_hover_square()

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

# update logic for each frame
def update_pass(events):
    # check for mouse click
    if current_turn == PLAYER:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_player_input(event.pos[0], event.pos[1])
    else:
        handle_cpu_input()

    pass

# called every single frame until game exits
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
        render_pass()


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
