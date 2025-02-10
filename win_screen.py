import pygame
from settings import FONTS


def show_win_screen(screen, level):
    screen.fill("white")

    width, height = screen.get_size()

    if level == 1:
        title = "Level 1 Complete!"
    elif level == 2:
        title = "Level 2 Complete!"
    elif level == 3:
        title = "Level 3 Complete!"
    else:
        title = "You Won!"

    text = FONTS["title"].render(title, True, "black")
    text_rect = text.get_rect(center=(width // 2, height // 3))
    screen.blit(text, text_rect)

    next_button_text = FONTS["button"].render("Next", True, "black")
    next_button_rect = next_button_text.get_rect(center=(width // 2, height // 2))
    quit_text = FONTS["button"].render("Quit", True, "black")
    quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 100))

    screen.blit(next_button_text, next_button_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    return True
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    return False
