"""
Game Rewrite (Began October 29th, 2024)

Authors:

Gavin Conley
Trevor Williams
Lucas Allen

"""

from abc import abstractmethod, ABC
from gc import enable

import pygame
import random
import math

# Init pygame lib
pygame.init()
# Constant values (never change)
# Usually denoted in ALL CAPS
WIDTH = 1280
HEIGHT = 720

game_score = 0

PLAYER_SPEED = 5.0
BULLET_SPEED = 30.0
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRASS_GREEN = (60, 179, 113)
# Init pygame and our font
pygame.init()

# Pygame constants
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()

FONT = pygame.font.Font("assets/pokemonFont.ttf", 32)
FONT_SMALL = pygame.font.Font("assets/pokemonFont.ttf", 20)
# Used for score points and stuff
FONT_TINY = pygame.font.Font("assets/pokemonFont.ttf", 12)

BACKDROP = pygame.image.load("assets/background.png")
BACKDROP = pygame.transform.scale(BACKDROP, (WIDTH, HEIGHT))

# Zombie images
ZOMB_SPRITES = [
    pygame.image.load("assets/Zombie_1.png").convert_alpha(),
    pygame.image.load("assets/Zombie_2.png").convert_alpha(),
    pygame.image.load("assets/Zombie_3.png").convert_alpha(),
    pygame.image.load("assets/Zombie_4.png").convert_alpha()
]

# Sound effects
SOUND_SHOOT = pygame.mixer.Sound("assets/shoot2.wav")
SOUND_DEATH = pygame.mixer.Sound("assets/death.wav")
SOUND_HURT = pygame.mixer.Sound("assets/hurt.wav")
SOUND_PLAYER_HURT = pygame.mixer.Sound("assets/player_hurt.wav")
SOUND_WIN = pygame.mixer.Sound("assets/vicroy.wav")
SOUND_SCORE_ADD = pygame.mixer.Sound("assets/score_add2.wav")
SOUND_CHEAT_ENABLE = pygame.mixer.Sound("assets/cheat.wav")
SOUND_UPGRADE = pygame.mixer.Sound("assets/upgrade.wav")

TAG_PLAYER = "player"
TAG_ZOMBIE = "zombie"
TAG_BULLET = "bullet"

# When true, draws debug hitboxes around all characters
show_debug_hitboxes = False
enable_developer_cheats = False

dimming = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

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
        self.stop()
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
        # the "dead" variable tells the game whether this gameObject should be deleted
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
        self.p_surf = pygame.image.load("assets/Chardle_Small.png").convert_alpha()
        self.p_surf = pygame.transform.scale(self.p_surf, p_rect.size)
        self.health = 100.0
        self.hurt_timer = Stopwatch()
        self.hurt_timer.start()
        # Timer for bullet sounds, so they don't overplay when full auto is used
        self.sound_timer = Stopwatch()
        self.sound_timer.start()
        super().__init__(p_rect, self.p_surf, TAG_PLAYER)


    def render(self, display_screen):
        debug_surface = pygame.Surface((self.rect.w, self.rect.h))
        debug_surface.fill(WHITE)
        display_screen.blit(self.surface, self.rect.topleft)
        # temporarily disabled that until we fix the textures
        #super().render(display_screen)


    def update(self, events, keys, scene):
        global game_score

        if self.health <= 0.0:
            self.dead = True
            DEATH.set_score(game_score)
            change_scene("death")
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
                self.p_surf = pygame.transform.flip(self.p_surf, True, False)
                self.facing_right = False

        if keys[pygame.K_d] and self.rect.right < WIDTH:
            dx += PLAYER_SPEED
            if not self.facing_right:
                self.p_surf = pygame.transform.flip(self.p_surf, True, False)
                self.facing_right = True

        # Flip our sprite depending on which way we move

        self.rect.move_ip(dx, dy)

        if not WORLD.full_auto_enabled:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen_pos = event.pos
                    self.shoot(screen_pos[0], screen_pos[1])
        else:
            if pygame.mouse.get_pressed()[0]:
                screen_pos = pygame.mouse.get_pos()
                self.shoot(screen_pos[0], screen_pos[1])


        if self.hurt_timer.has_passed(250):
            self.surface = self.p_surf


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

        if self.sound_timer.has_passed(75):
            SOUND_SHOOT.play(0)
            self.sound_timer.restart()

        current_scene.game_objects.append(Bullet(px, py, mx, my, WORLD.ricochet_enabled))



    def on_hurt(self, zombie):
        # Hurting the player
        if self.hurt_timer.has_passed(750):
            self.health -= 12.5
            SOUND_PLAYER_HURT.play(0)
            self.hurt_timer.restart()

            red = pygame.Surface(self.rect.size)
            red.fill(RED)
            self.surface = red



"""
The bullet does not rely on the Rect class for its position,
because the Rect class only uses ints and not floats,
we need floats to be more precise.

Before this change the aiming was terribly imprecise,
especially at diagonal angles.
"""
class Bullet(GameObject, ABC):
    def __init__(self, x, y, motion_x: float, motion_y: float, has_ricochet = False):
        self.size = 5
        self.has_ricochet = has_ricochet

        b_rect = pygame.Rect(x, y, self.size, self.size)
        b_surf = pygame.Surface(b_rect.size)
        b_surf.fill((255, 255, 0))

        self.pos_x = x
        self.pos_y = y

        self.motion_x = motion_x
        self.motion_y = motion_y

        self.times_bounced = 0

        super().__init__(b_rect, b_surf, TAG_BULLET)


    def render(self, display_screen):
        display_screen.blit(self.surface, (self.pos_x - (self.size / 2), self.pos_y - (self.size / 2)))


    def update(self, events, key, scene):
        self.pos_x += self.motion_x
        self.pos_y += self.motion_y

        if not is_within_bounds(self.pos_x, self.pos_y):
            if self.has_ricochet:
                self.bounce()
            else:
                self.dead = True

        if self.times_bounced >= 2:
            self.dead = True

        self.rect = pygame.Rect(self.pos_x - 2.5, self.pos_y - 2.5, 5.0, 5.0)
        # Loop through each zombie to see if we hit and kill
        for obj in scene.game_objects:
            if obj.tag != TAG_ZOMBIE:
                continue

            if self.has_ricochet:
                if obj.rect.colliderect(self.rect):
                    self.bounce()
                    obj.on_shot()
            else:
                if obj.rect.collidepoint(self.pos_x, self.pos_y):
                    # Kill zombie
                    obj.on_shot()
                    # Kill bullet
                    self.dead = True
                    break

    def bounce(self):
        self.times_bounced += 1
        self.motion_x *= -1
        self.motion_y *= -1

    def on_death(self):
        pass


class Zombie(GameObject, ABC):

    movement_speed = 3.5

    def __init__(self, x, y):
        self.zomb_type = random.randint(1, 4)
        self.max_hits = 1 if self.zomb_type != 4 else 2
        w = 40 if self.zomb_type != 4 else 90
        h = 60 if self.zomb_type != 4 else 90
        z_rect = pygame.Rect(x, y, w, h)
        z_surf = ZOMB_SPRITES[self.zomb_type - 1]
        z_surf = pygame.transform.scale(z_surf, z_rect.size)

        super().__init__(z_rect, z_surf, TAG_ZOMBIE)

        self.death_stopwatch = Stopwatch()
        self.hurt_cooldown = Stopwatch()
        self.hurt_cooldown.start()
        # Default/placeholder values for the direction, will be instantly changed on first update of zombie
        # Typically either 1 or -1 or 0
        self.x_dir = 0
        self.y_dir = 0

        self.shot = False
        self.hits_taken = 0
        # We face
        self.facing_right = True


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
        if self.hurt_cooldown.has_passed(100):
            self.hits_taken += 1
            self.hurt_cooldown.restart()
            if not self.shot and self.max_hits <= self.hits_taken:
                self.surface.fill((255, 0, 0))
                self.shot = True
                self.death_stopwatch.start()

                if type(current_scene) is World:
                    current_scene.score_queue.append(50 if self.zomb_type != 4 else 100)
        SOUND_HURT.play(0)


    def on_death(self):
        SOUND_DEATH.play(0)
        if type(current_scene) == World:
            if WORLD.vamp_enabled:
                WORLD.player.health = min(WORLD.player.health + 0.1, 100.0)

            current_scene.kill_count += 1
            current_scene.zombie_count -= 1


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

    square1 = pygame.Rect(100, HEIGHT * 6 // 8, 100, 120)
    square2 = pygame.Rect(100, HEIGHT * 6 // 8, 100, 120)
    square3 = pygame.Rect(100, HEIGHT * 6 // 8, 100, 120)
    square4 = pygame.Rect(100, HEIGHT * 6 // 8, 100, 120)

    square_distance = 100
    dist_from_man = 170

    square_speed = 5
    chasing = True

    square1_img_right = pygame.image.load("assets/CharIdleRight.png").convert_alpha()
    square1_img_right = pygame.transform.scale(square1_img_right, (square1.width, square1.height))
    square1_img = square1_img_right  # Start with the right-facing image

    square2_img_right = pygame.image.load("assets/Zombie_1.png").convert_alpha()
    square2_img_right = pygame.transform.scale(square2_img_right, (square2.width, square2.height))
    square2_img = square2_img_right  # Start with right-facing image

    square3_img_right = pygame.image.load("assets/Zombie_3.png")
    square3_img_right = pygame.transform.scale(square3_img_right, (square3.width, square3.height))
    square3_img = square3_img_right

    square4_img_right = pygame.image.load("assets/Zombie_Hurt2.png")
    square4_img_right = pygame.transform.scale(square4_img_right, (square4.width, square4.height))
    square4_img = square4_img_right

    title_text = FONT.render("Survive the Night", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    start_text = FONT.render("Start", True, RED)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def __init__(self):
        super().__init__("menu")
        pygame.mixer.init()
        self.intro_sound = pygame.mixer.Sound("assets/Scary⧸Tense Music - ＂Look Behind You＂.wav")
        self.intro_sound.set_volume(2)
        self.intro_playing = False
        self.start_sound()

    def start_sound(self):
        if not self.intro_playing:
            self.intro_sound.play(loops=1)
            self.intro_playing = True

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
        display_screen.blit(self.square3_img, self.square3)
        display_screen.blit(self.square4_img, self.square4)


        display_screen.blit(self.title_text, self.title_rect)
        display_screen.blit(self.start_text, self.start_rect)


    def chasing_images(self):
        if self.chasing:
            self.square1.x -= self.square_speed  # Move left
            self.square2.x = self.square1.x + self.square_distance
            self.square3.x = self.square1.x + self.dist_from_man
            self.square4.x = self.square3.x + self.square_distance
                #IMAGE FLIP
            self.square1_img = pygame.transform.flip(self.square1_img_right, True, False)
            self.square2_img = pygame.transform.flip(self.square2_img_right, True, False)
            self.square3_img = pygame.transform.flip(self.square3_img_right, True, False)
            self.square4_img = self.square4_img_right

            if self.square2.x < -self.square_distance:
                self.chasing = False
        else:
            self.square1.x += self.square_speed  # Move right
            self.square2.x = self.square1.x - self.square_distance
            self.square3.x = self.square1.x - self.dist_from_man
            self.square4.x = self.square3.x - self.square_distance
                    #IMAGE FLIP
            self.square1_img = self.square1_img_right
            self.square2_img = self.square2_img_right
            self.square3_img = self.square3_img_right
            self.square4_img = pygame.transform.flip(self.square4_img_right, True, False)

            if self.square1.x > WIDTH:
                self.chasing = True

    def stop_sound(self):
        if self.intro_playing:
            self.intro_sound.stop()
            self.intro_playing = False

    def reset_sound(self):
        self.intro_playing = False

    def update_scene(self, events, keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_rect.collidepoint(event.pos):
                    self.stop_sound()
                    change_scene("world")


""" End Main Menu """

""" Begin World """

class World(Scene, ABC):

    # Hard zombie limit, to prevent lag or whatever
    ZOMBIE_LIMIT = 75

    # Debug/developer variables
    draw_tracer = False
    # Wave is 20 seconds long
    wave_length = 20 * 1000
    bypass_wave = False

    full_auto_enabled = False
    vamp_enabled = False
    ricochet_enabled = False


    def __init__(self):
        super().__init__("world")
        self.player = Player()
        self.current_wave = 0
        self.spawn_timer = Stopwatch()
        self.zombie_count = 0
        self.kill_count = 0

        self.should_spawn_zombies = False
        """ Survival wave variables section """

        # timers
        self.score_add_delay = Stopwatch()

        self.wave_timer = Stopwatch()
        self.wave_countdown = Stopwatch()

        # flag variables
        self.wave_starting = False
        self.wave_active = False
        self.should_start_next_wave = False

        # Begin wave 1 when we start of course
        self.set_start_wave()

        self.score_queue = []


    def draw_scene(self, display_screen):
        global show_debug_hitboxes, WHITE, game_score, WIDTH, HEIGHT, dimming
        # Backdrop
        display_screen.blit(BACKDROP, (0, 0))

        dimming.fill((0, 0, 0, 64))
        display_screen.blit(dimming, (0, 0))

        # Player hitbox (if applicable)
        if show_debug_hitboxes:
            player_box = pygame.Surface(self.player.rect.size)
            player_box.fill((255, 0, 255))
            display_screen.blit(player_box, self.player.rect.topleft)

        # Draw player
        self.player.render(display_screen)

        # Draw zombies and bullets
        for obj in self.game_objects:
            if show_debug_hitboxes:
                hitbox = pygame.Surface((obj.rect.w + 2, obj.rect.h + 2))
                hitbox.fill((255, 0, 0))
                display_screen.blit(hitbox, (obj.rect.x - 1, obj.rect.y - 1))

            obj.render(display_screen)


        """ User interface and overlay stuff """

        # Draw tracer line
        if self.draw_tracer:
            pygame.draw.line(display_screen, (196, 64, 64), self.player.rect.center, pygame.mouse.get_pos())

        """ General stats """
        wave_counter = FONT_SMALL.render(f"Wave: {self.current_wave}", True, WHITE)
        display_screen.blit(wave_counter, (4, 4))

        kill_counter = FONT_SMALL.render(f"Kills: {self.kill_count}", True, WHITE)
        display_screen.blit(kill_counter, (4, 28))

        """ Wave indicators """
        if self.wave_starting:
            countdown = max(0.0, round((3000 - self.wave_countdown.elapsed_time()) / 1000.0, 1))
            countdown_text = FONT.render(f"Wave starting in {countdown}s...",
                                         True, WHITE)
            display_screen.blit(countdown_text, (WIDTH / 2 - (countdown_text.get_width() / 2),
                                                 HEIGHT / 2 - (countdown_text.get_height() / 2)))
        elif self.wave_active:
            wave_remaining = max(0.0, round((self.wave_length / 1000.0) - (self.wave_timer.elapsed_time() / 1000.0), 1))
            remaining_text = FONT_SMALL.render(f"{wave_remaining} seconds left in wave {self.current_wave}", True, WHITE)
            display_screen.blit(remaining_text, (WIDTH / 2 - (remaining_text.get_width() / 2), 4))

        """ Health and score points """

        health = self.player.health
        red = ((100.0 - health) / 100.0) * 255
        green = (health / 100.0) * 255
        health_text = FONT_SMALL.render(f"Health: {round(health, 1)}", True, (int(red), int(green), 0))
        display_screen.blit(health_text, (4, HEIGHT - 4 - health_text.get_height()))

        score_text = FONT_SMALL.render(f"Score: {game_score}", True, WHITE)
        display_screen.blit(score_text, (4, HEIGHT - score_text.get_height() - health_text.get_height() - 8))

        y_offset = 0
        for i in range(len(self.score_queue)):
            score = self.score_queue[i]
            text = FONT_SMALL.render(f"+{score}", True, (255, 0, 0))
            display_screen.blit(text, (4, HEIGHT - score_text.get_height() - health_text.get_height() - text.get_height() - 12 - y_offset))
            y_offset += (4 + text.get_height())


    def update_scene(self, events, keys):
        global game_score, show_debug_hitboxes, enable_developer_cheats

        # initial start

        # Score counting
        if len(self.score_queue) != 0:
            self.score_add_delay.start()

            delay = max(750 - (len(self.score_queue) * 50), 25)
            if self.score_add_delay.has_passed(delay):
                # pygame.mixer.Sound.play(SOUND_SCORE_ADD, 0)
                game_score += self.score_queue[0]
                self.score_queue.pop(0)
                self.score_add_delay.stop()

        # Begin countdown
        if self.should_start_next_wave:
            if self.current_wave > 0:
                SOUND_WIN.play(0)
                current_scene.score_queue.append(1000)

            self.should_start_next_wave = False
            self.wave_starting = True
            self.wave_countdown.start()

        # Post countdown
        if self.wave_starting and self.wave_countdown.has_passed(3000):

            self.wave_countdown.stop()
            self.wave_starting = False

            self.current_wave += 1

            self.should_spawn_zombies = True
            self.wave_active = True

            self.wave_timer.start()

        # Post wave
        if self.wave_active and self.wave_timer.has_passed(self.wave_length) or self.bypass_wave:
            self.bypass_wave = False

            self.wave_active = False
            self.wave_timer.stop()

            self.should_spawn_zombies = False
            self.game_objects.clear()

            for value in self.score_queue:
                game_score += value

            self.score_queue.clear()
            # Upgrade menu
            change_scene("upgrades")


        for event in events:
            if event.type == pygame.KEYDOWN:
                if enable_developer_cheats:
                    match event.key:
                        case pygame.K_r:
                            self.reset()
                        case pygame.K_x:
                            change_scene("death")
                        case pygame.K_h:
                            show_debug_hitboxes = not show_debug_hitboxes
                        case pygame.K_j:
                            self.bypass_wave = True
                else:
                    if event.key == pygame.K_BACKSLASH:
                        enable_developer_cheats = True
                        SOUND_CHEAT_ENABLE.play(0)
                    elif event.key == pygame.K_ESCAPE:
                        change_scene("menu")

        # Calculate duration of our spawn delay based on what wave we are
        n = self.current_wave * 375
        # The absolute shortest delay is 100 ms
        delay = max(2500 - n, 50)

        # Spawn zombies when needed
        if self.spawn_timer.has_passed(delay):
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


    def set_start_wave(self):
        self.should_start_next_wave = True

""" End World """


class DeathScreen(Scene, ABC):

    def __init__(self):
        super().__init__("death")
        self.restart_text = FONT.render("Press 'R' to Restart", True, WHITE)
        self.quit_text = FONT.render("Press 'Q' to Quit", True, WHITE)
        self.game_over = FONT.render("Game Over", True, RED)

        global game_score
        self.score_text = FONT.render(f"Score: {game_score}", True, WHITE)

        self.game_over_rect = self.game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.score_rect = self.score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.restart_rect = self.restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        pygame.mixer.init()
        self.end_sound = pygame.mixer.Sound('assets/Horror Scary Ghost Sound Effects.wav')
        self.end_sound.set_volume(0.5)
        self.end_playing = False

    def start_scene(self):
        if not self.end_playing:
            self.end_sound.play(loops=1)
            self.end_playing = True

    def update_scene(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.start_new_game()  # Restart the game
                elif event.key == pygame.K_q:
                    global running
                    running = False  # Quit the game
        self.start_scene()

    def draw_scene(self, display_screen):
        display_screen.fill(BLACK)
        display_screen.blit(self.game_over, self.game_over_rect)
        display_screen.blit(self.score_text, self.score_rect)
        display_screen.blit(self.restart_text, self.restart_rect)
        display_screen.blit(self.quit_text, self.quit_rect)

    def stop_sound(self):
        if self.end_playing:
            self.end_sound.stop()
            self.end_playing = False

    def start_new_game(self):
        global current_scene
        WORLD.reset()
        change_scene("world")
        pygame.mixer.stop()

    def set_score(self, score):
        self.score_text = FONT.render(f"Score: {score}", True, WHITE)

    def reset_sound(self):
        self.end_playing = False

class UpgradeScreen(Scene, ABC):

    def __init__(self):
        super().__init__("upgrades")

        self.next_wave_rect = pygame.Rect(WIDTH / 2 - 300, HEIGHT - (HEIGHT / 6), 600, 100)
        self.next_wave_surf = pygame.Surface(self.next_wave_rect.size)
        self.next_wave_surf.fill((0, 255, 0))

        self.next_wave_text = FONT.render("Start next wave!", True, BLACK)
        self.buy_upgrades_text = FONT_SMALL.render("Buy upgrades:", True, WHITE)

        self.auto_rect = None
        self.vamp_rect = None
        self.ricochet_rect = None


    def update_scene(self, events, keys):
        global game_score

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.next_wave_rect.collidepoint(event.pos):
                    change_scene("world")
                    WORLD.set_start_wave()
                elif self.auto_rect.collidepoint(event.pos) and game_score >= 5000:
                    WORLD.full_auto_enabled = True
                    game_score -= 5000
                    SOUND_UPGRADE.play(0)
                elif self.vamp_rect.collidepoint(event.pos) and game_score >= 10000:
                    WORLD.vamp_enabled = True
                    game_score -= 10000
                    SOUND_UPGRADE.play(0)
                elif self.ricochet_rect.collidepoint(event.pos) and game_score >= 15000:
                    WORLD.ricochet_enabled = True
                    game_score -= 15000
                    SOUND_UPGRADE.play(0)

        pass


    def draw_scene(self, display_screen):
        global BACKDROP, dimming

        display_screen.blit(BACKDROP, (0, 0))
        dimming.fill((0, 0, 0, 192))
        display_screen.blit(dimming, (0, 0))

        title_text = FONT.render(f"Wave {WORLD.current_wave} cleared!", True, WHITE)
        title_x = (WIDTH / 2) - (title_text.get_width() / 2)
        title_y = 24
        display_screen.blit(title_text, (title_x, title_y))


        display_screen.blit(self.next_wave_surf, self.next_wave_rect.topleft)
        display_screen.blit(self.next_wave_text,
                            (
                                (WIDTH / 2) - (self.next_wave_text.get_width() / 2), self.next_wave_rect.centery - (self.next_wave_text.get_height() / 2)
                            )
        )

        """ The following code is pretty stupid, don't recommend viewing """

        # Full auto upgrade button
        text_color = (255, 0, 0)
        if WORLD.full_auto_enabled:
            text_color = (0, 255, 0)
        elif game_score >= 5000:
            text_color = (96, 128, 96)

        auto_text = FONT.render("Full auto upgrade - 5000 pts", True, text_color)
        a_x = (WIDTH / 2) - (auto_text.get_width() / 2)
        a_y = 140
        if self.auto_rect is None:
            self.auto_rect = pygame.Rect(a_x, a_y, auto_text.get_width(), auto_text.get_height())
        display_screen.blit(auto_text, (a_x, a_y))

        # Vampire upgrade button

        text_color = (255, 0, 0)
        if WORLD.vamp_enabled:
            text_color = (0, 255, 0)
        elif game_score >= 10000:
            text_color = (96, 128, 96)

        vamp_text = FONT.render("Vampire upgrade - 10000 pts", True, text_color)
        v_x = (WIDTH / 2) - (vamp_text.get_width() / 2)
        v_y = 240
        if self.vamp_rect is None:
            self.vamp_rect = pygame.Rect(v_x, v_y, vamp_text.get_width(), vamp_text.get_height())
        display_screen.blit(vamp_text, (v_x, v_y))

        # Ricochet upgrade button

        text_color = (255, 0, 0)
        if WORLD.ricochet_enabled:
            text_color = (0, 255, 0)
        elif game_score >= 15000:
            text_color = (96, 128, 96)

        ricochet_text = FONT.render("Ricochet upgrade - 15000 pts", True, text_color)
        r_x = (WIDTH / 2) - (ricochet_text.get_width() / 2)
        r_y = 340
        if self.ricochet_rect is None:
            self.ricochet_rect = pygame.Rect(r_x, r_y, ricochet_text.get_width(), ricochet_text.get_height())
        display_screen.blit(ricochet_text, (r_x, r_y))


        """ Score render"""
        score_text = FONT_SMALL.render(f"Points: {game_score}", True, WHITE)
        display_screen.blit(score_text, ((WIDTH / 2) - (score_text.get_width() / 2), 460))



# This Section is for game scenes and variables, not stuff needed explicitly in each level or in the gameplay itself
MAIN_MENU = MainMenu()  # "menu"
WORLD = World()         # "world"
DEATH = DeathScreen()
UPGRADES = UpgradeScreen()
# death state not added yet lol

scenes = {
    MAIN_MENU.name: MAIN_MENU,
    WORLD.name: WORLD,
    DEATH.name: DEATH,
    UPGRADES.name: UPGRADES
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
    if isinstance(current_scene, DeathScreen):
        current_scene.reset_sound()
        current_scene.start_scene()
    else:
        if hasattr(current_scene, 'stop_sound'):
            current_scene.stop_sound()


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
