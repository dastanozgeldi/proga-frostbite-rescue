import pygame


pygame.init()
SCREEN = pygame.display.set_mode()
pygame.display.set_caption("Frostbite Rescue")

FPS = 60
FONTS = {
    "title": pygame.font.Font(None, 120),
    "medium": pygame.font.Font(None, 50),
    "small": pygame.font.Font(None, 30),
    "button": pygame.font.Font(None, 60),
}
