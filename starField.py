import pygame
import random


class starField():
    def doStars(amount, width, height):
        background = pygame.Surface((width, height), pygame.SRCALPHA)
        for x in range(amount):
            if x % 1 == 0:
                color = (255, 255, 255)
            if x % 2 == 0:
                color = (255, 210, 140)
            if x % 3 == 0:
                color = (169, 151, 192)
            posX = random.randrange(1, width)
            posY = random.randrange(1, height)
            starSize = random.randrange(0, 3)
            pygame.draw.circle(background, (color),
                               (posX, posY), starSize, 0)
            background.set_alpha(150)
        return background
