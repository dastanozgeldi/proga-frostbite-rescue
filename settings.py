import pygame


pygame.init()
TITLE = "Frostbite Rescue: Muzbek"
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)

FPS = 60
FONTS = {
    "title": pygame.font.Font(None, 120),
    "medium": pygame.font.Font(None, 50),
    "small": pygame.font.Font(None, 30),
    "button": pygame.font.Font(None, 60),
}
