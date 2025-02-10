import sys
import pygame
from animal import Animal
from player import Player
from settings import FONTS, FPS
from wall import Wall


class Level: 
    def __init__(self, screen, level_number, level_layout=None):
        self.screen = screen
        self.level_number = level_number

        self.walls = []
        self.animals = []

        self.exit_rect = None
        x = y = 0
        for row in level_layout:
            for col in row:
                if col == "W":
                    Wall((x, y), self.walls)
                elif col == "E":
                    self.exit_rect = pygame.Rect(x, y, 64, 64)
                elif col == "A":
                    Animal((x, y), self.animals)
                x += 64
            y += 64
            x = 0

        self.player = Player(screen, pos=(128, 128))
        self.score = 0

        self.running = True

    def loop(self, clock):
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dx = 0
            dy = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                dx = -8
            if keys[pygame.K_d]:
                dx = 8
            if keys[pygame.K_w]:
                dy = -8
            if keys[pygame.K_s]:
                dy = 8

            # Use the unified move method with wall and animal collision handling.
            self.player.move(dx, dy, self.walls, self.animals)

            # End level when the player reaches the exit.
            if self.exit_rect and self.player.rect.colliderect(self.exit_rect):
                self.running = False

            self.screen.fill("white")

            for wall in self.walls:
                pygame.draw.rect(self.screen, "black", wall.rect)

            if self.exit_rect:
                pygame.draw.rect(self.screen, (255, 0, 0), self.exit_rect)

            for animal in self.animals:
                self.screen.blit(animal.image, animal.rect)

            self.screen.blit(self.player.image, self.player.rect)

            level_text = FONTS["medium"].render(f"Level: {self.level_number}", True, (107, 142, 35))
            self.screen.blit(level_text, (10, 10))

            # Draw the held animal attached to the player's hand (with rescue counter).
            if self.player.held_animal:
                held_rect = self.player.held_animal.get_rect()
                held_rect.center = (self.player.rect.left - 5, self.player.rect.centery + 5)
                self.screen.blit(self.player.held_animal, held_rect)
                count_text = FONTS["small"].render(str(self.score), True, "black")
                count_rect = count_text.get_rect()
                count_rect.bottomright = (held_rect.left + 10, held_rect.bottom)
                self.screen.blit(count_text, count_rect)

            pygame.display.flip()
