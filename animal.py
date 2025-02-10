import pygame


class Animal:
    def __init__(self, pos, animals):
        self.image_trapped = pygame.image.load("assets/trapped.png")
        self.image_rescued = pygame.image.load("assets/rescued.png")
        self.image_trapped = pygame.transform.scale(self.image_trapped, (64, 64))
        self.image_rescued = pygame.transform.scale(self.image_rescued, (64, 64))
        self.image = self.image_trapped
        self.rect = self.image.get_rect(topleft=pos)
        self.rescued = False
        animals.append(self)

    def rescue(self):
        self.image = self.image_rescued
        self.rescued = True
