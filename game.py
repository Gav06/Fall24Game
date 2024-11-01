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
import math

# Init pygame lib
pygame.init()
# Constant values (never change)
# Usually denoted in ALL CAPS
WIDTH = 1280
HEIGHT = 720

PLAYER_SPEED = 5
BULLET_SPEED = 20
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRASS_GREEN = (60, 179, 113)
# Init pygame and our font
pygame.init()
FONT = pygame.font.Font("assets/pokemonFont.ttf", 32)

# Sound effects
SOUND_SHOOT = pygame.mixer.Sound("assets/shoot2.wav")
SOUND_DEATH = pygame.mixer.Sound("assets/death.wav")
SOUND_HURT = pygame.mixer.Sound("assets/hurt.wav")

TAG_PLAYER = "player"
TAG_ZOMBIE = "zombie"
TAG_BULLET = "bullet"

# Pygame constants
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Used for animations and stuff
class Stopwatch:

    current_ms = 0

    def start(self):
        self.reset()


    def reset(self):
        self.current_ms = pygame.time.get_ticks()


    def has_passed(self, ms):
        return self.elapsed_time() >= ms

    def elapsed_time(self):
        return pygame.time.get_ticks() - self.current_ms


# Starts with a plain white surface
class GameObject:
    def __init__(self, rect, surf, tag):
        self.tag = tag
        self.rect = rect
        self.surface = surf
        # the "dead" variable tells the game whether or not this gameObject should be deleted
        self.dead = False

    # "target" parameter is going to be the screen, or whatever surface we will blit onto
    def render(self, display_screen):
        display_screen.blit(self.surface, (self.rect.x, self.rect.y))

    # "events" parameter is the event list from the pygame loop
    @abstractmethod
    def update(self, events, keys, scene):
        pass

    @abstractmethod
    def on_death(self):
        pass


class Player(GameObject, ABC):
    # Our player texture is facing right by default
    facing_right = True

    def __init__(self):
        p_rect = pygame.Rect(WIDTH // 2 - 20 // 2, HEIGHT // 2 - 20 // 2, 24, 48)
        p_surf = pygame.image.load("assets/Chardle_Small.png").convert_alpha()
        p_surf = pygame.transform.scale(p_surf, p_rect.size)
        super().__init__(p_rect, p_surf, TAG_PLAYER)


    def render(self, display_screen):
        debug_surface = pygame.Surface((self.rect.w, self.rect.h))
        debug_surface.fill(WHITE)
        display_screen.blit(self.surface, self.rect.topleft)
        # temporarily disabled that until we fix the textures
        #super().render(display_screen)


    def update(self, events, keys, scene):
        # Player move input
        dx = 0
        dy = 0

        if keys[pygame.K_w] and self.rect.top > 0:
            dy += -PLAYER_SPEED

        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            dy += PLAYER_SPEED

        if keys[pygame.K_a] and self.rect.left > 0:
            dx += -PLAYER_SPEED
            if self.facing_right:
                self.surface = pygame.transform.flip(self.surface, True, False)
                self.facing_right = False

        if keys[pygame.K_d] and self.rect.right < WIDTH:
            dx += PLAYER_SPEED
            if not self.facing_right:
                self.surface = pygame.transform.flip(self.surface, True, False)
                self.facing_right = True

        # Flip our sprite depending on which way we move

        self.rect.move_ip(dx, dy)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen_pos = event.pos
                self.shoot(screen_pos[0], screen_pos[1])


    # Fires a projectile with the current load-out towards the current position
    def shoot(self, x, y):

        px = self.rect.centerx
        py = self.rect.centery

        dx = x - px
        dy = y - py

        h = math.sqrt(dx**2 + dy**2)

        mx = (dx / h) * BULLET_SPEED
        my = (dy / h) * BULLET_SPEED

        pygame.mixer.Sound.play(SOUND_SHOOT, 0)
        current_scene.game_objects.append(Bullet(px, py, mx, my))


    def on_death(self):
        pass


class Bullet(GameObject, ABC):
    def __init__(self, x, y, motion_x, motion_y):
        b_rect = pygame.Rect(x, y, 5, 5)
        b_surf = pygame.Surface(b_rect.size)
        b_surf.fill((255, 255, 0))
        super().__init__(b_rect, b_surf, TAG_BULLET)

        self.motion_x = motion_x
        self.motion_y = motion_y


    def render(self, display_screen):
        super().render(display_screen)

    def update(self, events, key, scene):
        self.rect.move_ip(self.motion_x, self.motion_y)

        if not is_within_bonuds(self.rect.x, self.rect.y):
            self.dead = True
            return

        # Loop through each zombie to see if we hit and kill
        for obj in scene.game_objects:
            if obj.tag != TAG_ZOMBIE:
                continue

            if self.rect.colliderect(obj.rect):
                # Kill zombie
                obj.on_shot()
                # Kill bullet
                self.dead = True
                break


    def on_death(self):
        pass


class Zombie(GameObject, ABC):

    shot = False
    movement_speed = 3.5

    def __init__(self):
        z_rect = pygame.Rect(0, 0, 20, 20)
        z_surf = pygame.Surface(z_rect.size)
        z_surf.fill((32, 255, 32))

        super().__init__(z_rect, z_surf, TAG_ZOMBIE)

        self.death_stopwatch = Stopwatch()


    def render(self, display_screen):
        super().render(display_screen)


    def update(self, events, keys, scene):
        if type(current_scene) is not World:
            return

        if self.shot:
            if self.death_stopwatch.has_passed(250):
                self.dead = True

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
        else:
            dx = 0

        # if player is above us
        if py < zy:
            dy *= -1
        # if player is below
        elif py > zy:
            dy *= 1
        else:
            dy = 0

        # Move towards the player
        self.rect.move_ip(dx, dy)

    def on_shot(self):
        if not self.shot:
            self.surface.fill((255, 0, 0))
            self.shot = True
            self.death_stopwatch.start()

        pygame.mixer.Sound.play(SOUND_HURT, 0)

    def on_death(self):
        pygame.mixer.Sound.play(SOUND_DEATH, 0)
        pass


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

    square1 = pygame.Rect(100, HEIGHT * 6 // 8, 70, 90)
    square2 = pygame.Rect(100, HEIGHT * 6 // 8, 70, 90)
    square_distance = 90
    square_speed = 2
    chasing = True

    square1_img = pygame.image.load("assets/CharIdleRight.png").convert_alpha()
    square1_img = pygame.transform.scale(square1_img, (square1.width, square1.height))
    square2_img = pygame.image.load("assets/Zombie_One.png").convert_alpha()
    square2_img = pygame.transform.scale(square2_img, (square2.width, square2.height))

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

            pygame.draw.circle(display_screen, WHITE, self.star_list[i], 2)

        display_screen.blit(self.square2_img, self.square2)

        display_screen.blit(self.square2_img, self.square2)

        self.chasing_images()
        display_screen.blit(self.square1_img, self.square1)
        display_screen.blit(self.square2_img, self.square2)

        display_screen.blit(self.title_text, self.title_rect)
        display_screen.blit(self.start_text, self.start_rect)

    def chasing_images(self):
        if self.chasing:
            self.square1.x -= self.square_speed
            self.square2.x = self.square1.x + self.square_distance

            if self.square2.x < -self.square_distance:
                self.chasing = False
        else:
            self.square1.x += self.square_speed
            self.square2.x = self.square1.x - self.square_distance

            if self.square1.x > WIDTH:
                self.chasing = True


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
        self.player.update(events, keys, self)

        for obj in self.game_objects:
            obj.update(events, keys, self)

            if obj.dead:
                obj.on_death()
                continue


        # Re-setting the list to one without all the dead gameObjects
        # (cleanup of out-of-bounds bullets and dead zombies)

        self.game_objects = [obj for obj in self.game_objects if not obj.dead]



""" End World """

# This Section is for game scenes and variables, not stuff needed explicitly in each level or in the gameplay itself
MAIN_MENU = MainMenu()  # "menu"
WORLD = World()         # "world"
# DEATH = Death()       # "death"
# death state not added yet lol

scenes = {
    MAIN_MENU.name: MAIN_MENU,
    WORLD.name: WORLD
    # GAMEOVER.name : GAMEOVER
}


running = True
# Our scene is Main menu by default
current_scene = scenes["menu"]
frame_timer = Stopwatch()

def is_within_bonuds(x, y):
    return 0 < x < WIDTH and 0 < y < HEIGHT

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
        frame_timer.reset()

        # Updates
        update_pass()
        render_pass(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        print(f"Frame time {frame_timer.elapsed_time()}ms")


def __main__():
    game_init()
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    __main__()