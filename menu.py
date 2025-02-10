
import pygame
from settings import FONTS


def show_main_menu(screen):
    screen.fill("white")
    title_text = FONTS["title"].render("Frostbite Rescue", True, "black")
    title_rect = title_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 3 - 50)
    )
    play_text = FONTS["button"].render("Play", True, "black")
    play_rect = play_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )
    quit_text = FONTS["button"].render("Quit", True, "black")
    quit_rect = quit_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 100)
    )

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return True
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    return False
