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
        self.thaw_progress = 0  # New attribute
        self.required_thaw = 100  # New attribute
        animals.append(self)

    def update_thaw(self, amount):
        if not self.rescued:
            self.thaw_progress = min(self.required_thaw, self.thaw_progress + amount)
            if self.thaw_progress >= self.required_thaw:
                self.rescue()

    def rescue(self):
        self.image = self.image_rescued
        self.rescued = True
        self.thaw_progress = self.required_thaw
