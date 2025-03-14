import pygame
from level import Level
from menu import show_main_menu
from settings import SCREEN
from win_screen import show_win_screen

clock = pygame.time.Clock()


levels = [
    [
        "WWWWWWWWWWWWWWWWWWWWWW",
        "W                    W",
        "W          A         W",
        "W                    W",
        "W                    W",
        "W               A    W",
        "W   A                W",
        "W                    W",
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
        "W   A     W   WWWWW  W",
        "W   WWW    I         W",
        "W   WWWW  IAI  W     W",
        "W   W      I WWWWWW  W",
        "W WWW  WWWW          W",
        "WWW   W   WWWWW W    W",
        "W   W     W W   AI   W",
        "W   WWW WWW   W W    W",
        "W     W   W   W W    W",
        "W W      WW  IIAI    W",
        "W W   WWWW   WWW  WW W",
        "W          E         W",
        "WWWWWWWWWWWWWWWWWWWWWW",
    ],
]


def run_game():
    show_main_menu(SCREEN)

    for i in range(len(levels)):
        level = Level(SCREEN, i + 1, levels[i])
        level.loop(clock)

    # All levels complete, show win screen
    show_win_screen(SCREEN)


if __name__ == "__main__":
    run_game()
