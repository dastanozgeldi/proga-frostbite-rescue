import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, pos=None):
        super().__init__()
        # Load and scale the player image.
        self.image = pygame.image.load("assets/muzbek.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        # If no starting position is provided, center on screen.
        if pos is None:
            width, height = screen.get_size()
            pos = (width // 2, height // 2)
        self.rect = self.image.get_rect(center=pos)

        # Default speed (used in Level 1); Level 2 movement uses manual dx/dy.
        self.speed = 5

        # Attributes used in the labyrinth (Level 2)
        self.rescue_count = 0
        self.held_animal = None

        self.heat_ray_active = False
        self.heat_ray_pos = (0, 0)
        self.heat_ray_color = (255, 0, 0)  # Red
        self.thaw_rate = 0.5

        # Key sprites for visual feedback when moving (Level 1).
        self.key_sprites = {
            pygame.K_a: pygame.image.load("assets/a_key.png"),
            pygame.K_s: pygame.image.load("assets/s_key.png"),
            pygame.K_d: pygame.image.load("assets/d_key.png"),
            pygame.K_w: pygame.image.load("assets/w_key.png"),
        }
        for key in self.key_sprites:
            self.key_sprites[key] = pygame.transform.scale(
                self.key_sprites[key], (50, 50)
            )
        self.current_key_sprite = None

    def update_heat_ray(self, mouse_pos):
        self.heat_ray_pos = mouse_pos
        self.heat_ray_active = pygame.mouse.get_pressed()[0]  # Left click

    def update(self, keys, walls=None, animals=None):
        """
        Update movement based on key presses.
        For Level 1, call this with just the keys.
        For Level 2, you can pass walls and animals to handle collisions.
        """
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_a]
        elif keys[pygame.K_d]:
            dx = self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_d]
        elif keys[pygame.K_w]:
            dy = -self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_w]
        elif keys[pygame.K_s]:
            dy = self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_s]
        else:
            self.current_key_sprite = None

        self.move(dx, dy, walls, animals)

    def move(self, dx, dy, walls=None, animals=None, ice_blocks=None):
        """Moves the player by dx and dy while handling collisions if provided."""
        if dx != 0:
            self.move_single_axis(dx, 0, walls, animals, ice_blocks)
        if dy != 0:
            self.move_single_axis(0, dy, walls, animals, ice_blocks)

    def move_single_axis(self, dx, dy, walls=None, animals=None, ice_blocks=None):
        self.rect.x += dx
        self.rect.y += dy

        # Collision with walls
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    if dx < 0:
                        self.rect.left = wall.rect.right
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    if dy < 0:
                        self.rect.top = wall.rect.bottom

        # Collision with ice blocks
        if ice_blocks:
            for ice in ice_blocks:
                if self.rect.colliderect(ice.rect):
                    if dx > 0:
                        self.rect.right = ice.rect.left
                    if dx < 0:
                        self.rect.left = ice.rect.right
                    if dy > 0:
                        self.rect.bottom = ice.rect.top
                    if dy < 0:
                        self.rect.top = ice.rect.bottom

        # Collision with animals - only collect if already rescued
        if animals:
            for animal in animals[:]:
                if (
                    self.rect.colliderect(animal.rect)
                    and animal.rescued
                    and not animal.collected
                ):
                    animal.collected = True
                    self.rescue_count += 1
                    self.held_animal = pygame.transform.scale(
                        animal.image_rescued, (50, 50)
                    )
                    animals.remove(animal)

    def apply_heat_ray(self, animals, ice_blocks):
        if self.heat_ray_active:
            ray_start = (self.rect.centerx, self.rect.centery)

            # Apply to animals
            for animal in animals:
                if not animal.rescued:
                    distance = (
                        (self.heat_ray_pos[0] - animal.rect.centerx) ** 2
                        + (self.heat_ray_pos[1] - animal.rect.centery) ** 2
                    ) ** 0.5
                    if distance < 50:
                        animal.update_thaw(self.thaw_rate)

            # Apply to ice blocks
            for ice in ice_blocks[
                :
            ]:  # Use slice copy since we might modify during iteration
                distance = (
                    (self.heat_ray_pos[0] - ice.rect.centerx) ** 2
                    + (self.heat_ray_pos[1] - ice.rect.centery) ** 2
                ) ** 0.5
                if distance < 50:
                    if ice.update_thaw(self.thaw_rate):
                        ice_blocks.remove(ice)
