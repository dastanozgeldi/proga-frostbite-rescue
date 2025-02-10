import pygame

class Ice:
    def __init__(self, pos, ice_blocks):
        self.rect = pygame.Rect(pos[0], pos[1], 64, 64)
        self.thaw_progress = 0
        self.required_thaw = 100  # Same as animals for consistency
        ice_blocks.append(self)

    def update_thaw(self, amount):
        self.thaw_progress = min(self.required_thaw, self.thaw_progress + amount)
        return self.thaw_progress >= self.required_thaw
