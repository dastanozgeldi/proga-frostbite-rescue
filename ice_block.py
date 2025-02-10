
import pygame


class IceBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.trapped_image = pygame.image.load("assets/trapped.png")
        self.trapped_image = pygame.transform.scale(self.trapped_image, (64, 64))

        self.rescued_image = pygame.image.load("assets/rescued.png")
        self.rescued_image = pygame.transform.scale(self.rescued_image, (64, 64))

        self.image = self.trapped_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.melted = False

    def melt(self):
        if not self.melted:
            self.image = self.rescued_image
            self.melted = True
            return 1
        return 0
