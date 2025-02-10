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
        self.running = True

    def loop(self, clock):
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle movement
            dx = dy = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: dx = -8
            if keys[pygame.K_d]: dx = 8
            if keys[pygame.K_w]: dy = -8
            if keys[pygame.K_s]: dy = 8

            # Update player position and heat ray
            self.player.move(dx, dy, self.walls, self.animals)
            self.player.update_heat_ray(pygame.mouse.get_pos())
            self.player.apply_heat_ray(self.animals)

            # Drawing
            self.screen.fill("white")

            # Draw walls
            for wall in self.walls:
                pygame.draw.rect(self.screen, "black", wall.rect)

            # Draw exit
            if self.exit_rect:
                pygame.draw.rect(self.screen, (255, 0, 0), self.exit_rect)

            # Draw animals and their thaw progress bars
            for animal in self.animals:
                self.screen.blit(animal.image, animal.rect)
                if not animal.rescued:
                    # Draw thaw progress bar above animal
                    bar_width = 64  # Same as animal width
                    bar_height = 5
                    bar_pos = (animal.rect.x, animal.rect.y - 10)
                    
                    # Background bar
                    pygame.draw.rect(self.screen, "gray", 
                        (bar_pos[0], bar_pos[1], bar_width, bar_height))
                    
                    # Progress bar
                    progress_width = (animal.thaw_progress / animal.required_thaw) * bar_width
                    if progress_width > 0:
                        pygame.draw.rect(self.screen, "red",
                            (bar_pos[0], bar_pos[1], progress_width, bar_height))

            # Draw player
            self.screen.blit(self.player.image, self.player.rect)

            # Draw heat ray if active
            if self.player.heat_ray_active:
                pygame.draw.line(self.screen, self.player.heat_ray_color,
                            (self.player.rect.centerx, self.player.rect.centery),
                            self.player.heat_ray_pos, 2)

            # Draw UI elements
            level_text = FONTS["medium"].render(f"Level: {self.level_number}", True, (107, 142, 35))
            self.screen.blit(level_text, (10, 10))

            pygame.display.flip()