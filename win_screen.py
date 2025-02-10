import pygame
from settings import FONTS


def show_win_screen(screen):
    screen.fill("white")

    width, height = screen.get_size()

    text = FONTS["title"].render("You Won!", True, "black")
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    quit_text = FONTS["button"].render("Quit", True, "black")
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 50))

    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
