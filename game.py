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

PLAYER_SPEED = 5.0
BULLET_SPEED = 20.0
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRASS_GREEN = (60, 179, 113)
# Init pygame and our font
pygame.init()
FONT = pygame.font.Font("assets/pokemonFont.ttf", 32)
FONT_SMALL = pygame.font.Font("assets/pokemonFont.ttf", 20)

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

# When true, draws debug hitboxes around all characters
SHOW_DEBUG_HITBOXES = False

# Used for animations and stuff
class Stopwatch:

    def __init__(self):
        self.current_ms = 0
        self.started = False

    def start(self):
        if not self.started:
            self.started = True
            self.reset()


    def stop(self):
        self.started = False


    def reset(self):
        self.current_ms = pygame.time.get_ticks()


    def restart(self):
        self.reset()
        self.start()


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
        self.health = 100.0
        self.hurt_timer = Stopwatch()
        super().__init__(p_rect, p_surf, TAG_PLAYER)


    def render(self, display_screen):
        debug_surface = pygame.Surface((self.rect.w, self.rect.h))
        debug_surface.fill(WHITE)
        display_screen.blit(self.surface, self.rect.topleft)
        # temporarily disabled that until we fix the textures
        #super().render(display_screen)


    def update(self, events, keys, scene):
        if self.health <= 0.0:
            self.dead = True

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
        # Bullet mathematics
        px = self.rect.centerx
        py = self.rect.centery
        dx = x - px
        dy = y - py
        # Make sure we don't divide by zero (if mouse is EXACTLY on top of our character)
        dx = 1.0 if dx == 0.0 else dx
        dy = 1.0 if dy == 0.0 else dy

        h = math.sqrt(pow(dx, 2.0) + pow(dy, 2.0))

        mx = (dx / h) * BULLET_SPEED
        my = (dy / h) * BULLET_SPEED

        pygame.mixer.Sound.play(SOUND_SHOOT, 0)
        current_scene.game_objects.append(Bullet(px, py, mx, my))


    def on_death(self):
        pass


    def on_hurt(self, zombie):
        self.hurt_timer.start()

        if self.hurt_timer.has_passed(750):
            self.health -= 20.0
            pygame.mixer.Sound.play(SOUND_HURT, 0)
            self.hurt_timer.stop()


"""
The bullet does not rely on the Rect class for its position,
because the Rect class only uses ints and not floats,
we need floats to be more precise.

Before this change the aiming was terribly imprecise,
especially at diagonal angles.
"""
class Bullet(GameObject, ABC):
    def __init__(self, x, y, motion_x: float, motion_y: float):
        self.size = 5

        b_rect = pygame.Rect(x, y, self.size, self.size)
        b_surf = pygame.Surface(b_rect.size)
        b_surf.fill((255, 255, 0))

        self.pos_x = x
        self.pos_y = y

        self.motion_x = motion_x
        self.motion_y = motion_y

        super().__init__(b_rect, b_surf, TAG_BULLET)


    def render(self, display_screen):
        display_screen.blit(self.surface, (self.pos_x - (self.size / 2), self.pos_y - (self.size / 2)))


    def update(self, events, key, scene):
        self.pos_x += self.motion_x
        self.pos_y += self.motion_y

        if not is_within_bounds(self.pos_x, self.pos_y):
            self.dead = True
            return

        # Loop through each zombie to see if we hit and kill
        for obj in scene.game_objects:
            if obj.tag != TAG_ZOMBIE:
                continue

            if obj.rect.collidepoint(self.pos_x, self.pos_y):
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

    def __init__(self, x, y):
        z_rect = pygame.Rect(x, y, 20, 20)
        z_surf = pygame.Surface(z_rect.size)
        z_surf.fill((32, 255, 32))

        super().__init__(z_rect, z_surf, TAG_ZOMBIE)

        self.death_stopwatch = Stopwatch()
        # Default/placeholder values for the direction, will be instantly changed on first update of zombie
        # Typically either 1 or -1 or 0
        self.x_dir = 0
        self.y_dir = 0


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

        # Find which way we will move towards player
        if px < zx:
            self.x_dir = -1
        elif px > zx:
            self.x_dir = 1
        else:
            self.x_dir = 0

        if py < zy:
            self.y_dir = -1
        elif py > zy:
            self.y_dir = 1
        else:
            self.y_dir = 0

        dx *= self.x_dir
        dy *= self.y_dir

        # Move towards the player
        self.rect.move_ip(dx, dy)


        if self.rect.colliderect(player):
            player.on_hurt(self)

    def on_shot(self):
        if not self.shot:
            self.surface.fill((255, 0, 0))
            self.shot = True
            self.death_stopwatch.start()

        pygame.mixer.Sound.play(SOUND_HURT, 0)

    def on_death(self):
        pygame.mixer.Sound.play(SOUND_DEATH, 0)
        if type(current_scene) == World:
            current_scene.kill_count += 1
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

    square1_img_right = pygame.image.load("assets/CharIdleRight.png").convert_alpha()
    square1_img_right = pygame.transform.scale(square1_img_right, (square1.width, square1.height))
    square1_img = square1_img_right  # Start with the right-facing image

    square2_img_right = pygame.image.load("assets/Zombie_One.png").convert_alpha()
    square2_img_right = pygame.transform.scale(square2_img_right, (square2.width, square2.height))
    square2_img = square2_img_right  # Start with right-facing image

    title_text = FONT.render("Survive the Night", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    start_text = FONT.render("Start", True, RED)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def __init__(self):
        super().__init__("menu")
        pygame.mixer.init()
        self.image2_sound = pygame.mixer.Sound('assets/Zombie sound effect.wav')
        self.sound_playing = False
        self.image2_sound.set_volume(0.75)

    def draw_scene(self, display_screen):
        display_screen.fill(BLACK)

        quarter_rect = pygame.Rect(0, HEIGHT * 3 // 4, WIDTH, HEIGHT // 4)
        pygame.draw.rect(display_screen, GRASS_GREEN, quarter_rect)

        for i, (stars_x, stars_y) in enumerate(self.star_list):
            self.star_list[i] = (stars_x - 0.45, stars_y)

            if stars_x < 0:
                self.star_list[i] = (WIDTH, random.randint(0, HEIGHT * 3 // 4))

            pygame.draw.circle(display_screen, WHITE, self.star_list[i], 2)

        self.chasing_images()

        display_screen.blit(self.square1_img, self.square1)
        display_screen.blit(self.square2_img, self.square2)

        if self.square2.colliderect(quarter_rect):
            self.play_sound()
        else:
            self.stop_sound()

        display_screen.blit(self.title_text, self.title_rect)
        display_screen.blit(self.start_text, self.start_rect)


    def chasing_images(self):
        if self.chasing:
            self.square1.x -= self.square_speed  # Move left
            self.square2.x = self.square1.x + self.square_distance
                #IMAGE FLIP
            self.square1_img = pygame.transform.flip(self.square1_img_right, True, False)
            self.square2_img = pygame.transform.flip(self.square2_img_right, True, False)

            if self.square2.x < -self.square_distance:
                self.chasing = False
        else:
            self.square1.x += self.square_speed  # Move right
            self.square2.x = self.square1.x - self.square_distance
                    #IMAGE FLIP
            self.square1_img = self.square1_img_right
            self.square2_img = self.square2_img_right

            if self.square1.x > WIDTH:
                self.chasing = True

    image2_sound = pygame.mixer.Sound('assets/Zombie sound effect.wav')   #IMPORT SOUND
    sound_playing = False
    def play_sound(self):
        if not self.sound_playing:
            self.image2_sound.play(1)
            self.sound_playing = True


    def stop_sound(self):
        if self.sound_playing:
            self.image2_sound.stop()
            self.sound_playing = False


    def update_scene(self, events, keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(event.pos):
                    # Switch to level
                    self.stop_sound()
                    change_scene("world")

""" End Main Menu """

""" Begin World """

class World(Scene, ABC):

    # Hard zombie limit, to prevent lag or whatever
    ZOMBIE_LIMIT = 50

    # Debug/developer variables
    should_spawn_zombies = True
    draw_tracer = False

    def __init__(self):
        super().__init__("world")
        self.player = Player()
        self.current_wave = 0
        self.spawn_timer = Stopwatch()
        self.zombie_count = 0
        self.kill_count = 0
        # Each wave is 30 seconds (30,000ms)
        self.wave_length = 20 * 1000
        self.wave_timer = Stopwatch()
        self.wave_countdown = Stopwatch()


    def draw_scene(self, display_screen):
        global SHOW_DEBUG_HITBOXES, WHITE
        # Backdrop
        display_screen.fill(BLACK)

        # Player hitbox (if applicable)
        if SHOW_DEBUG_HITBOXES:
            player_box = pygame.Surface(self.player.rect.size)
            player_box.fill((255, 0, 255))
            display_screen.blit(player_box, self.player.rect.topleft)

        # Draw player
        self.player.render(display_screen)

        # Draw zombies and bullets
        for obj in self.game_objects:
            if SHOW_DEBUG_HITBOXES:
                hitbox = pygame.Surface((obj.rect.w + 2, obj.rect.h + 2))
                hitbox.fill((255, 0, 0))
                display_screen.blit(hitbox, (obj.rect.x - 1, obj.rect.y - 1))

            obj.render(display_screen)

        # Draw overlays and stuff

        # Draw tracer line
        if self.draw_tracer:
            pygame.draw.line(display_screen, (196, 64, 64), self.player.rect.center, pygame.mouse.get_pos())

        wave_counter = FONT_SMALL.render(f"Wave: {self.current_wave}", True, WHITE)
        display_screen.blit(wave_counter, (4, 4))

        kill_counter = FONT_SMALL.render(f"Kills: {self.kill_count}", True, WHITE)
        display_screen.blit(kill_counter, (4, 28))

        if self.wave_countdown.started:
            countdown_text = FONT.render(f"Wave starting in {3000 - self.wave_countdown.elapsed_time()}ms...",
                                         True, WHITE)
            display_screen.blit(countdown_text, (WIDTH / 2 - (countdown_text.get_width() / 2),
                                                 HEIGHT / 2 - (countdown_text.get_height() / 2)))


    def update_scene(self, events, keys):
        # initial start
        if self.current_wave == 0:
            self.start_next_wave()

        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_r:
                        self.reset()
                    case pygame.K_ESCAPE:
                        change_scene("menu")


        # Spawn zombies when needed
        if self.spawn_timer.has_passed(2500):
            self.spawn_zombie_random()
            self.spawn_timer.restart()


        # Update player, zombies, and bullets
        self.player.update(events, keys, self)

        for obj in self.game_objects:
            obj.update(events, keys, self)

            if obj.dead:
                obj.on_death()
                if type(obj) == Zombie:
                    self.zombie_count -= 1
                continue


        # Re-setting the list to one without all the dead gameObjects
        # (cleanup of out-of-bounds bullets and dead zombies)

        self.game_objects = [obj for obj in self.game_objects if not obj.dead]


    def reset(self):
        self.game_objects.clear()
        self.__init__()

    # Called many times throughout the course of a wave, spawns a random zombie in a random location about the player
    def spawn_zombie_random(self):
        if self.zombie_count >= self.ZOMBIE_LIMIT or (not self.should_spawn_zombies):
            return

        # Set our initial spawn position to the player so we guarantee the loop to run
        spawn_x = self.player.rect.x
        spawn_y = self.player.rect.y
        min_dist = 100

        # Find a good Y
        while abs(self.player.rect.x - spawn_x) < min_dist:
            spawn_x = random.randint(0, WIDTH)

        # Find a good X
        while abs(self.player.rect.y - spawn_y) < min_dist:
            spawn_y = random.randint(0, HEIGHT)

        self.game_objects.append(Zombie(spawn_x, spawn_y))
        self.zombie_count += 1


    def start_next_wave(self):
        pass

""" End World """

class DeathScreen(Scene, ABC):

    def __init__(self, name):
        super().__init__(name)

    def update_scene(self, events, keys):
        pass


    def draw_scene(self, display_screen):
        pass


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

# Takes in 2 positions, both a tuple of: (int, int), returns a float (i think)
def distance(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def is_within_bounds(x, y):
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
        frame_timer.restart()

        # Updates
        update_pass()
        render_pass(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        #print(f"Frame time {frame_timer.elapsed_time()}ms")


def __main__():
    game_init()
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    __main__()
