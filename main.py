import pygame
import time
import random
import starField
import ExtractSprite

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

# Load player ship sprites =
player_ship = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/PlayerShip.png').convert_alpha())

# Load enemies
enemy01 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy01.png').convert_alpha())

enemy02 = ExtractSprite.ExtractSprite(
    pygame.image.load('Resources/Sprites/Enemy02.png').convert_alpha())

explosionimg = pygame.image.load(
    'Resources/Sprites/Explosion.png').convert_alpha()

# Projectile list
projectile = []
enemy_protectile = []

# Enemy list
enemies = []

# Load sounds
laser = pygame.mixer.Sound("Resources/Sounds/LaserShoot01.wav")
explosion = pygame.mixer.Sound("Resources/Sounds/Explosion01.wav")
player_hit = pygame.mixer.Sound("Resources/Sounds/PlayerHit.wav")
upgrade = pygame.mixer.Sound("Resources/Sounds/Upgrade.wav")
weapon_up = pygame.mixer.Sound("Resources/Sounds/WeaponUp.wav")

# Play BGM
pygame.mixer.init()
pygame.mixer.music.load("Resources/Sounds/bgm.mp3")
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

# Player start position
x = 0
y = (DISPLAY_HEIGHT - 64) / 2

# Sprite frames
player_frame_list = []
enemy01_frame_list = []
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

add_enemy = pygame.USEREVENT
pygame.time.set_timer(add_enemy, 2000)


def play_sound(src):
    pygame.mixer.Sound.stop
    pygame.mixer.Sound.play(src)


def draw_enemy():
    y = random.randrange(64, 704)
    new_enemy = pygame.Rect(1000, y, 20, 20)
    enemies.append(new_enemy)


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
                pygame.mixer.Sound.play(laser)


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
    if score == 10:
        pygame.mixer.Sound.stop
        pygame.mixer.Sound.play(upgrade)
        num_bullets += 2


def check_enemies():
    global score
    global playsound
    global p_health
    enemyhit = 0
    # Enemy list
    for do_enemy in enemies[:]:
        # Check if list contains anything
        if len(enemies) > 0:
            for check_projectile in projectile[:]:
                # Check if colllide with projectile, if so, remove
                if do_enemy.colliderect(check_projectile):
                    display_area.blit(
                        explosionimg, (do_enemy[0], do_enemy[1]+10))
                    enemies.remove(do_enemy)
                    score += 1
                    play_sound(explosion)
                    check_score()
            # Enemy is off screen so remove from list
            if do_enemy[0] <= -64:
                enemies.remove(do_enemy)
            # Draw enemies
            display_area.blit(enemy01_frame_list[curr_frame],
                              (do_enemy[0], do_enemy[1]))
            # Move enemy across x, towards player.
            do_enemy[0] -= enemy_speed
            # Move enemy towards player
            if do_enemy[1] < y:
                do_enemy[1] += 2
            if do_enemy[1] > y:
                do_enemy[1] -= 2
            # Enemy collided with player sprite.
            if do_enemy.colliderect(player_rect):
                display_area.blit(
                    explosionimg, (do_enemy[0], do_enemy[1]+10))
                enemies.remove(do_enemy)
                play_sound(player_hit)
                p_health -= 10


running = True
while running:
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
        if event.type == add_enemy:
            draw_enemy()
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()
pygame.quit()
