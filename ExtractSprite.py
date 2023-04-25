import pygame


class ExtractSprite():
    def __init__(self, image):
        self.image = image

    def extract_sprite(self, frame):
        sprite = pygame.sprite.Sprite()
        sprite = pygame.Surface((32, 32)).convert_alpha()
        sprite.blit(self.image, (0, 0), (0, frame * 32, 32, 32))
        sprite = pygame.transform.scale_by(sprite, 2)
        sprite.set_colorkey(0)

        return sprite
