import sys
import pygame
from animal import Animal
from ice import Ice
from player import Player
from settings import FONTS, FPS
from wall import Wall


class Level:
    def __init__(self, screen, level_number, level_layout=None):
        self.screen = screen
        self.level_number = level_number

        self.walls = []
        self.animals = []
        self.ice_blocks = []  # New list for ice blocks

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
                elif col == "I":
                    Ice((x, y), self.ice_blocks)
                x += 64
            y += 64
            x = 0

        self.player = Player(screen, pos=(128, 128))
        self.running = True

    def are_all_animals_collected(self):
        return len(self.animals) == 0  # Since we remove animals when collected

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
            if keys[pygame.K_a]:
                dx = -8
            if keys[pygame.K_d]:
                dx = 8
            if keys[pygame.K_w]:
                dy = -8
            if keys[pygame.K_s]:
                dy = 8

            # Update player position and check ice block collisions
            self.player.move(dx, dy, self.walls, self.animals, self.ice_blocks)
            self.player.update_heat_ray(pygame.mouse.get_pos())

            # Apply heat ray to both animals and ice
            self.player.apply_heat_ray(self.animals, self.ice_blocks)

            # Check for level completion
            if self.exit_rect and self.player.rect.colliderect(self.exit_rect):
                if self.are_all_animals_collected():
                    self.running = False

            # Drawing
            self.screen.fill("white")

            # Draw walls
            for wall in self.walls:
                pygame.draw.rect(self.screen, "black", wall.rect)

            # Draw exit - change color based on whether it's active
            if self.exit_rect:
                if self.are_all_animals_collected():
                    # Active exit - bright red
                    pygame.draw.rect(self.screen, (255, 0, 0), self.exit_rect)
                    # Optional: Add a glowing effect
                    pygame.draw.rect(
                        self.screen, (255, 100, 100), self.exit_rect.inflate(4, 4), 2
                    )
                else:
                    # Inactive exit - darker red/gray
                    pygame.draw.rect(self.screen, (128, 0, 0), self.exit_rect)

                    # Draw "locked" text above inactive exit
                    locked_text = FONTS["small"].render(
                        "Collect all animals!", True, (64, 64, 64)
                    )
                    text_rect = locked_text.get_rect(
                        midbottom=(self.exit_rect.centerx, self.exit_rect.top - 5)
                    )
                    self.screen.blit(locked_text, text_rect)

            for ice in self.ice_blocks[
                :
            ]:  # Use slice copy since we might modify during iteration
                # Draw ice block with slight transparency
                ice_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.rect(ice_surface, (150, 200, 255, 180), (0, 0, 64, 64))
                self.screen.blit(ice_surface, ice.rect)

                # Draw thaw progress bar
                bar_width = 64
                bar_height = 5
                bar_pos = (ice.rect.x, ice.rect.y - 10)

                # Background bar
                pygame.draw.rect(
                    self.screen, "gray", (bar_pos[0], bar_pos[1], bar_width, bar_height)
                )

                # Progress bar
                progress_width = (ice.thaw_progress / ice.required_thaw) * bar_width
                if progress_width > 0:
                    pygame.draw.rect(
                        self.screen,
                        (150, 200, 255),
                        (bar_pos[0], bar_pos[1], progress_width, bar_height),
                    )

            # Draw animals and their thaw progress bars
            for animal in self.animals:
                self.screen.blit(animal.image, animal.rect)
                if not animal.rescued:
                    bar_width = 64
                    bar_height = 5
                    bar_pos = (animal.rect.x, animal.rect.y + 5)

                    pygame.draw.rect(
                        self.screen,
                        "gray",
                        (bar_pos[0], bar_pos[1], bar_width, bar_height),
                    )

                    progress_width = (
                        animal.thaw_progress / animal.required_thaw
                    ) * bar_width
                    if progress_width > 0:
                        pygame.draw.rect(
                            self.screen,
                            "red",
                            (bar_pos[0], bar_pos[1], progress_width, bar_height),
                        )
                elif not animal.collected:
                    pygame.draw.circle(
                        self.screen,
                        "green",
                        (animal.rect.centerx, animal.rect.top + 5),
                        5,
                    )

            # Draw player
            self.screen.blit(self.player.image, self.player.rect)

            # Draw heat ray if active
            if self.player.heat_ray_active:
                pygame.draw.line(
                    self.screen,
                    self.player.heat_ray_color,
                    (self.player.rect.centerx, self.player.rect.centery),
                    self.player.heat_ray_pos,
                    2,
                )

            # Draw UI elements
            level_text = FONTS["medium"].render(
                f"Level: {self.level_number}", True, (107, 142, 35)
            )
            self.screen.blit(level_text, (10, 10))

            # Draw animals remaining counter
            animals_text = FONTS["small"].render(
                f"Animals remaining: {len(self.animals)}", True, "black"
            )
            self.screen.blit(animals_text, (10, 40))

            # Draw the held animal and rescue counter
            if self.player.held_animal:
                held_rect = self.player.held_animal.get_rect()
                held_rect.center = (
                    self.player.rect.left - 5,
                    self.player.rect.centery + 5,
                )
                self.screen.blit(self.player.held_animal, held_rect)
                count_text = FONTS["small"].render(
                    str(self.player.rescue_count), True, "black"
                )
                count_rect = count_text.get_rect()
                count_rect.bottomright = (held_rect.left + 5, held_rect.bottom)
                self.screen.blit(count_text, count_rect)

            pygame.display.flip()
