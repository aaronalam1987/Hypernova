import pygame
import ExtractSprite

# Load sounds
pygame.mixer.init()

sounds = {
    "laser": pygame.mixer.Sound("Resources/Sounds/LaserShoot01.wav"),
    "explosion": pygame.mixer.Sound("Resources/Sounds/Explosion01.wav"),
    "player_hit": pygame.mixer.Sound("Resources/Sounds/PlayerHit.wav"),
    "upgrade": pygame.mixer.Sound("Resources/Sounds/Upgrade.wav"),
    "weapon_up": pygame.mixer.Sound("Resources/Sounds/WeaponUp.wav"),
}

BGM = "Resources/Sounds/bgm.mp3"