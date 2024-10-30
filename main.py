import pygame
import time
import random
import starField
import ExtractSprite
from assets import sounds, BGM
import math

pygame.init()

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768

display_area = pygame.display.set_mode(
    (DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("HyperNova")
display_size = pygame.display.get_surface()

currWidth = display_size.get_width()
currHeight = display_size.get_height()

# Boundaries
xBound = currWidth - 64
yBound = currHeight - 64

run_game = 1

# Load player ship sprites =
player_ship = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/PlayerShip.png').convert_alpha())

# Load enemies
enemy01 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy01.png').convert_alpha())

enemy02 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy02.png').convert_alpha())

enemy03 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy03.png').convert_alpha())

enemy04 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy04.png').convert_alpha())

enemy05 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy05.png').convert_alpha())

explosionimg = pygame.image.load(
    'Resources/Sprites/Explosion.png').convert_alpha()

# Projectile list
projectile = []
enemy_protectile = []

# Enemy list
enemies = []

# Play BGM
pygame.mixer.music.load(BGM)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(0, 0)

# Create initial star field
star_field = starField.starField.doStars(200, currWidth, currHeight)

# Player speed
player_speed = 7

# Player bullet speed
p_bullet = 10

# Player health
p_health = 100

# Bullet amount
num_bullets = 3

# Enemy speed
enemy_speed = 10

# Init game time
init_time = pygame.time.get_ticks()

# Game time duration
anim_duration = 100  # (ms)

# Player start position, start far left and centre to screen 
x = 0
y = (DISPLAY_HEIGHT - 64) / 2

# Sprite frames
player_frame_list = []
enemy01_frame_list = []
enemy02_frame_list = []
enemy03_frame_list = []
enemy04_frame_list = []
enemy05_frame_list = []
number_frames = 3
bullet_speed = 250
curr_frame = 0

# Enemies killed
score = 0

# text
font = pygame.font.Font('Resources/Misc/SickleMoON.ttf', 32)


for x in range(number_frames):
    # Loop through number of frames and add to frame list
    player_frame_list.append(player_ship.extract_sprite(x))
    enemy01_frame_list.append(enemy01.extract_sprite(x))
    enemy02_frame_list.append(enemy02.extract_sprite(x))
    enemy03_frame_list.append(enemy03.extract_sprite(x))
    enemy04_frame_list.append(enemy04.extract_sprite(x))
    enemy05_frame_list.append(enemy05.extract_sprite(x))

add_enemy = pygame.USEREVENT
pygame.time.set_timer(add_enemy, 2000)


def play_sound(src):
    pygame.mixer.Sound.stop
    pygame.mixer.Sound.play(src)


def draw_enemy():
    y = random.randrange(64, 704)
    new_enemy = pygame.Rect(1000, y, 20, 20)
    enemy_type = random.choice([1, 2, 3, 4, 5])
    enemies.append((new_enemy, enemy_type))


def check_keys():
    global xBound
    global x
    global y

    key_press = pygame.key.get_pressed()
    # Check keypresses
    if x <= xBound:
        x += (key_press[pygame.K_RIGHT]) * player_speed
    if x > 0:
        x -= (key_press[pygame.K_LEFT]) * player_speed
    if y <= yBound:
        y += (key_press[pygame.K_DOWN]) * player_speed
    if y > 0:
        y -= (key_press[pygame.K_UP]) * player_speed
    # Spacepress = shoot, check vs animation duration and add "bullet" to projectile list
    if key_press[pygame.K_SPACE]:
        if current_time - init_time >= anim_duration:
            if len(projectile) < num_bullets:
                pygame.mixer.Sound.stop
                bullet = pygame.Rect(x + 64, y, 20, 20)
                projectile.append(bullet)
                pygame.mixer.Sound.play(sounds["laser"])


def animate(current_time):
    global star_field
    global curr_frame
    global init_time
    global anim_duration
    # Increment sprite animation frame and update starfield.
    if current_time - init_time >= anim_duration:
        curr_frame += 1
        init_time = current_time
        star_field = starField.starField.doStars(200, currWidth, currHeight)
        # Current frame is out of bounds of frame list, reset to 0
        if curr_frame >= len(player_frame_list):
            curr_frame = 0


def doprojectile():
  # Loop and draw projectile list
    for do_projectile in range(len(projectile)):
        pygame.draw.circle(display_area, (255, 0, 0),
                           (projectile[do_projectile][0], projectile[do_projectile][1] + 32), 3, 0)
        # Increment by projectile speed
        projectile[do_projectile][0] += p_bullet

    # Check if out of bounds & remove
    for check_projectile in projectile[:]:
        if check_projectile[0] > DISPLAY_WIDTH:
            projectile.remove(check_projectile)


def check_score():
    global num_bullets
    match score:
        case 10:
            num_bullets +=2
            pygame.mixer.Sound.stop
            pygame.mixer.Sound.play(sounds["upgrade"])
        case 20:
            num_bullets +=2
            pygame.mixer.Sound.stop
            pygame.mixer.Sound.play(sounds["upgrade"])    


def check_enemies():
    global score
    global playsound
    global p_health
    global enemy_speed
    enemyhit = 0
    # Enemy list
    for do_enemy, enemy_type in enemies[:]:
        # Check if list contains anything
        if len(enemies) > 0:
            for check_projectile in projectile[:]:
                # Check if colllide with projectile, if so, remove
                if do_enemy.colliderect(check_projectile):
                    display_area.blit(
                        explosionimg, (do_enemy[0], do_enemy[1]+10))
                    enemies.remove((do_enemy, enemy_type))
                    score += 1
                    play_sound(sounds["explosion"])
                    check_score()
                    if score > 10:
                        if len(enemies) <= 3: 
                            draw_enemy()
            # Enemy is off screen so remove from list
            if do_enemy[0] <= -64:
                enemies.remove((do_enemy, enemy_type))
            # Draw enemies
            match enemy_type:
                case 1:
                    display_area.blit(enemy01_frame_list[curr_frame], (do_enemy[0], do_enemy[1]))
                case 2:
                    display_area.blit(enemy02_frame_list[curr_frame], (do_enemy[0], do_enemy[1]))
                case 3:
                    display_area.blit(enemy03_frame_list[curr_frame], (do_enemy[0], do_enemy[1]))
                case 4:
                    display_area.blit(enemy04_frame_list[curr_frame], (do_enemy[0], do_enemy[1]))
                case 5:
                    display_area.blit(enemy05_frame_list[curr_frame], (do_enemy[0], do_enemy[1]))
            # Move enemy across x, towards player.
            do_enemy[0] -= enemy_speed
            # Move enemy towards player
            if do_enemy[1] < y:
                do_enemy[1] += 2
            if do_enemy[1] > y:
                do_enemy[1] -= 2
            # Enemy collided with player sprite.
            if do_enemy.colliderect(player_rect):
                match enemy_type:
                    case 5:
                        p_health += 10
                        display_area.blit(explosionimg, (do_enemy[0], do_enemy[1]+10))
                        enemies.remove((do_enemy, enemy_type))
                        play_sound(sounds["upgrade"])
                    case _:
                        display_area.blit(explosionimg, (do_enemy[0], do_enemy[1]+10))
                        enemies.remove((do_enemy, enemy_type))
                        play_sound(sounds["player_hit"])
                        p_health -= 10


def game_state():
    global p_health
    global run_game
    global score
    global bullet_speed
    global x
    global y
    if p_health == 0:
        text = font.render('GAME OVER', False, (255, 255, 255))
        display_area.blit(text, (350, 300))
        text = font.render('PRESS SPACE TO RESTART', False, (255, 255, 255))
        display_area.blit(text, (350, 400))
        run_game = 0

    if run_game == 0:
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_SPACE]:
            p_health = 100
            score = 0
            bullet_speed = 0
            run_game = 1
            x = 0
            y = (DISPLAY_HEIGHT - 64) / 2


running = True
while running:
    game_state()

    if run_game == 1:
        player_rect = pygame.Rect(x, y, 32, 32)

        # Get current time, used for animation frames / starfield
        current_time = pygame.time.get_ticks()
        sound_time = pygame.time.get_ticks()
        # Check for keypress to move player position
        check_keys()
        # Animates sprites/starfield
        animate(current_time)

        # Draw starfield and player
        display_area.fill((0, 0, 0))
        display_area.blit(star_field, (0, 0))
        display_area.blit(player_frame_list[curr_frame], (x, y))

        text = font.render('Score:  ' + str(score),
                           False, (255, 255, 255))
        display_area.blit(text, (10, 0))

        text = font.render('Health:  ' + str(p_health),
                           False, (255, 255, 255))
        text_rect = text.get_rect(center=(DISPLAY_WIDTH/2, 20))
        display_area.blit(text, text_rect)

        # Do bullets etc.
        doprojectile()
        # Check and draw enemies
        check_enemies()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == add_enemy and run_game == 1:
            draw_enemy()

    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
