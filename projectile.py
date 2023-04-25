import pygame


class projectile():

    def do_projectile(x, y):
        projectile = []
        projectile.append([x + 64, y])
        background = pygame.Surface((64, 64), pygame.SRCALPHA)
        for do_projectile in range(len(projectile)):
            pygame.draw.circle(background, (255, 0, 0), (
                projectile[do_projectile][0], projectile[do_projectile][1] + 32), 5, 0)
            # Increment by projectile speed
            projectile[do_projectile][0] += 3

        return background
