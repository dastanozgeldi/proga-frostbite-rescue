import pygame


class Wall:
    def __init__(self, pos, walls):
        self.rect = pygame.Rect(pos[0], pos[1], 64, 64)
        walls.append(self)
