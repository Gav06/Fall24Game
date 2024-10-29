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

# Constant values (never change)
# Usually denoted in ALL CAPS
MAIN_MENU = scene.MainMenu()

pygame.init()
width = 1280
height = 720
player_speed = 1
player = pygame.Rect(width // 2 - 20 // 2, height // 2 - 20 // 2, 20, 20)

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grass_green = (60, 179, 113)

font = pygame.font.Font("pokemonFont.ttf", 32)
screen = pygame.display.set_mode((width , height))
clock = pygame.time.Clock()
pygame.display.set_caption("Zombie Shooter")

menu = True
num_stars = 50
stars = [(random.randint(0, width), random.randint(0, height * 3 // 4)) for _ in range(num_stars)]
def draw_main_menu():
    screen.fill(black)

    quarter_rect = pygame.Rect(0, height * 3 // 4, width, height // 4)
    pygame.draw.rect(screen, grass_green, quarter_rect)
    for i, (stars_x, stars_y) in enumerate(stars):
        stars[i] = (stars_x - 0.45, stars_y)

        if stars_x < 0:
            stars[i] = (width, random.randint(0, height * 3 // 4))

        pygame.draw.circle(screen, white, stars[i], 2)  # Small white star

    title_text = font.render("Survive the Night", True, white)
    start_text = font.render("Start", True, red)
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
    start_rect = start_text.get_rect(center=(width // 2, height // 2 + 50))

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
        if keys[pygame.K_w] and player.top > 0:
            player.move_ip(0, -player_speed)
        if keys[pygame.K_s] and player.bottom < height:
            player.move_ip(0, player_speed)
        if keys[pygame.K_a] and player.left > 0:
            player.move_ip(-player_speed, 0)
        if keys[pygame.K_d] and player.right < width:
            player.move_ip(player_speed, 0)

        screen.fill(black)
        pygame.draw.rect(screen, white, player)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()