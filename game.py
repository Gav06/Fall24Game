"""
Game Rewrite (Began October 29th, 2024)

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

from abc import abstractmethod, ABC
import pygame
import random

from pygame import Surface

# Init pygame lib
pygame.init()
# Constant values (never change)
# Usually denoted in ALL CAPS
WIDTH = 1280
HEIGHT = 720

PLAYER_SPEED = 5
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRASS_GREEN = (60, 179, 113)
# Init pygame and our font
pygame.init()
FONT = pygame.font.Font("assets/pokemonFont.ttf", 32)

# Pygame constants
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Starts with a plain white surface
class GameObject:
    def __init__(self, rect, surf):
        self.rect = rect
        self.surface = surf

    # "target" parameter is going to be the screen, or whatever surface we will blit onto
    def render(self, display_screen):
        display_screen.blit(self.surface, (self.rect.x, self.rect.y))

    # "events" parameter is the event list from the pygame loop
    @abstractmethod
    def update(self, events, keys):
        pass


class Player(GameObject, ABC):
    def __init__(self):
        p_rect = pygame.Rect(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 20, 20)
        p_surf = pygame.image.load("assets/CharIdleRight.png").convert_alpha()
        super().__init__(p_rect, p_surf)


    def render(self, display_screen):
        debug_surface = pygame.Surface((self.rect.w, self.rect.h))
        debug_surface.fill(WHITE)
        display_screen.blit(debug_surface, self.rect.topleft)
        # temporarily disabled that until we fix the textures
        #super().render(display_screen)


    def update(self, events, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.move_ip(0, -PLAYER_SPEED)
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, PLAYER_SPEED)
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.move_ip(PLAYER_SPEED, 0)


class Zombie(GameObject, ABC):

    movement_speed = 1

    def __init__(self):
        z_rect = pygame.Rect(0, 0, 20, 20)
        z_surf = Surface(z_rect.size)
        z_surf.fill((32, 255, 32))
        super().__init__(z_rect, z_surf)


    def render(self, display_screen):
        super().render(display_screen)


    def update(self, events, keys):
        if type(current_scene) is not World:
            return

        player = current_scene.player
        zx = self.rect.x
        zy = self.rect.y

        px = player.rect.x
        py = player.rect.y

        dx = self.movement_speed
        dy = self.movement_speed

        # if player is to the left of us
        if px < zx:
            dx *= -1
        # if player is to the right
        elif px > zx:
            dx *= 1

        # if player is above us
        if py < zy:
            dy *= -1
        elif py > zy:
            dy *= 1

        self.rect.move_ip(dx, dy)


# Our class for each scene.
# The abstract methods are just methods that we will define in subclasses, at a later time
class Scene:
    # Empty list of GameObject instances
    game_objects = []

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def draw_scene(self, display_screen):
        pass


    @abstractmethod
    def update_scene(self, events, keys):
        pass

""" Begin Main Menu """

class MainMenu(Scene, ABC):

    star_count = 50
    star_list = [(random.randint(0, WIDTH), random.randint(0, HEIGHT * 3 // 4)) for _ in range(star_count)]

    title_text = FONT.render("Survive the Night", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    start_text = FONT.render("Start", True, RED)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def __init__(self):
        super().__init__("menu")


    def draw_scene(self, display_screen):
        display_screen.fill(BLACK)

        quarter_rect = pygame.Rect(0, HEIGHT * 3 // 4, WIDTH, HEIGHT // 4)
        pygame.draw.rect(display_screen, GRASS_GREEN, quarter_rect)

        for i, (stars_x, stars_y) in enumerate(self.star_list):
            self.star_list[i] = (stars_x - 0.45, stars_y)

            if stars_x < 0:
                self.star_list[i] = (WIDTH, random.randint(0, HEIGHT * 3 // 4))

            pygame.draw.circle(display_screen, WHITE, self.star_list[i], 2)  # Small white star

        display_screen.blit(self.title_text, self.title_rect)
        display_screen.blit(self.start_text, self.start_rect)


    def update_scene(self, events, keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(event.pos):
                    # Switch to level
                    change_scene("world")

""" End Main Menu """

""" Begin World """

class World(Scene, ABC):

    def __init__(self):
        super().__init__("world")
        self.player = Player()
        self.game_objects.append(Zombie())


    def draw_scene(self, display_screen):
        display_screen.fill(BLACK)
        self.player.render(display_screen)

        for obj in self.game_objects:
            obj.render(display_screen)


    def update_scene(self, events, keys):
        self.player.update(events, keys)

        for obj in self.game_objects:
            obj.update(events, keys)


""" End World """

# This Section is for game scenes and variables, not stuff needed explicitly in each level or in the gameplay itself
MAIN_MENU = MainMenu()  # "menu"
WORLD = World()         # "world"
# DEATH = Death()       # "death"
# death state not added yet lol

scenes = {
    MAIN_MENU.name: MAIN_MENU,
    WORLD.name: WORLD
    # DEATH.name: DEATH
}


running = True
# Our scene is Main menu by default
current_scene = scenes["menu"]

def change_scene(scene_name):
    global current_scene
    current_scene = scenes[scene_name]

def render_pass(display_screen):
    current_scene.draw_scene(display_screen)


def update_pass():
    global running

    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    current_scene.update_scene(events, keys)

def game_init():
    pygame.display.set_caption("Zombie Shooter")


def game_loop():
    global running

    while running:
        # Updates
        update_pass()
        render_pass(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)


def __main__():
    game_init()
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    __main__()