import sys
import pygame
from level import Level
from settings import FPS, SCREEN
from win_screen import show_win_screen

clock = pygame.time.Clock()


levels = [
    [
        "WWWWWWWWWWWWWWWWWWWWWW",
        "W                    W",
        "W          A   W     W",
        "W                    W",
        "W                    W",
        "W               A    W",
        "W   A         WWWWW  W",
        "W   WWW WWW          W",
        "W                    W",
        "W                    W",
        "W              A     W",
        "W       W WWW        W",
        "W       W  EW        W",
        "WWWWWWWWWWWWWWWWWWWWWW",
    ],
    [
        "WWWWWWWWWWWWWWWWWWWWWW",
        "W   WWW              W",
        "W   WWWW   A   W     W",
        "W   W        WWWWWW  W",
        "W WWW  WWWW          W",
        "W   W     W W   A    W",
        "W   A     W   WWWWW  W",
        "W   WWW WWW   W W    W",
        "W     W   W   W W    W",
        "WWW   W   WWWWW W    W",
        "W W      WW    A     W",
        "W W   WWWW   WWW     W",
        "W     W    E   W     W",
        "WWWWWWWWWWWWWWWWWWWWWW",
    ],
    [
        "WWWWWWWWWWWWWWWWWWWWWW",
        "W   WWW              W",
        "W   WWWW   A   W     W",
        "W   W        WWWWWW  W",
        "W WWW  WWWW          W",
        "W   W     W W   A    W",
        "W   A     W   WWWWW  W",
        "W   WWW WWW   W W    W",
        "W     W   W   W W    W",
        "WWW   W   WWWWW W    W",
        "W W      WW    A     W",
        "W W   WWWW   WWW     W",
        "W     W    E   W     W",
        "WWWWWWWWWWWWWWWWWWWWWW",
    ],
]


def run_game():
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if not show_win_screen(SCREEN, level=1):
            break
        level_1 = Level(SCREEN, 1, levels[0])
        level_1.update()

        # if not show_win_screen(SCREEN, level=2):
        #     break
        # level_2 = Level(SCREEN, 2, levels[1])
        # level_2.update()

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
