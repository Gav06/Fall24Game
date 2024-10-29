"""
Game Rewrite

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

import pygame
from pygame import Surface
import random
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

pygame.init()

# Constant values (never change)
# Usually denoted in ALL CAPS
MAIN_MENU = scene.MainMenu()
WIDTH = 1280
HEIGHT = 720
PLAYER_SPEED = 5
player_rect = pygame.Rect(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 20, 20)
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRASS_GREEN = (60, 179, 113)

font = pygame.font.Font("assets/pokemonFont.ttf", 32)
screen = pygame.display.set_mode((WIDTH , HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Zombie Shooter")

menu = True
num_stars = 50
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT * 3 // 4)) for _ in range(num_stars)]
def draw_main_menu():
    screen.fill(BLACK)

    quarter_rect = pygame.Rect(0, HEIGHT * 3 // 4, WIDTH, HEIGHT // 4)
    pygame.draw.rect(screen, GRASS_GREEN, quarter_rect)
    for i, (stars_x, stars_y) in enumerate(stars):
        stars[i] = (stars_x - 0.45, stars_y)

        if stars_x < 0:
            stars[i] = (WIDTH, random.randint(0, HEIGHT * 3 // 4))

        pygame.draw.circle(screen, WHITE, stars[i], 2)  # Small white star

    title_text = font.render("Survive the Night", True, WHITE)
    start_text = font.render("Start", True, RED)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

    return start_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if menu and event.type == pygame.MOUSEBUTTONDOWN:
            start_button = draw_main_menu()
            if start_button.collidepoint(event.pos):
                menu = False
    if menu:
        draw_main_menu()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.move_ip(0, -PLAYER_SPEED)
        if keys[pygame.K_s] and player_rect.bottom < HEIGHT:
            player_rect.move_ip(0, PLAYER_SPEED)
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_d] and player_rect.right < WIDTH:
            player_rect.move_ip(PLAYER_SPEED, 0)

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()