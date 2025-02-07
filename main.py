import pygame
import random
import sys  # needed for sys.exit()

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FONTS = {
    "title": pygame.font.Font(None, 120),
    "medium": pygame.font.Font(None, 50),
    "small": pygame.font.Font(None, 30),
    "button": pygame.font.Font(None, 60),
}

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Frostbite Rescue")

# ------------------------------------------------------------------
# Level 1 Classes (Sprite‑based)
# ------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width, height = screen.get_size()
        self.image = pygame.image.load("assets/muzbek.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.speed = 5

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

        # Holds the rescued (reduced) animal image.
        self.held_animal = None

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_a]
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_d]
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_w]
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.current_key_sprite = self.key_sprites[pygame.K_s]
        else:
            self.current_key_sprite = None


class IceBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.trapped_image = pygame.image.load("assets/trapped.png")
        self.trapped_image = pygame.transform.scale(self.trapped_image, (100, 100))

        self.rescued_image = pygame.image.load("assets/rescued.png")
        self.rescued_image = pygame.transform.scale(self.rescued_image, (100, 100))

        self.image = self.trapped_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.melted = False

    def melt(self):
        if not self.melted:
            self.image = self.rescued_image
            self.melted = True
            return 1
        return 0

# ------------------------------------------------------------------
# Main Menu and Win Screen Functions (Unified)
# ------------------------------------------------------------------

def show_main_menu():
    screen.fill(WHITE)
    title_text = FONTS["title"].render("Frostbite Rescue", True, BLACK)
    title_rect = title_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 3 - 50)
    )
    play_text = FONTS["button"].render("Play", True, BLACK)
    play_rect = play_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )
    quit_text = FONTS["button"].render("Quit", True, BLACK)
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


def display_score(screen_width, score):
    score_text = FONTS["medium"].render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))


def show_win_screen(score, level):
    screen.fill(WHITE)
    if level == 1:
        title = "Level 1 Complete!"
    elif level == 2:
        title = "Level 2 Complete!"
    else:
        title = "You Won!"
    text = FONTS["title"].render(title, True, BLACK)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    screen.blit(text, text_rect)

    # (For level 1, display the rescued score.)
    if level == 1 and score is not None:
        display_score(screen.get_width(), score)

    next_button_text = FONTS["button"].render("Next", True, BLACK)
    next_button_rect = next_button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    quit_text = FONTS["button"].render("Quit", True, BLACK)
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

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

# ------------------------------------------------------------------
# Level 1 Function (Frostbite Rescue)
# ------------------------------------------------------------------

def run_level_one():
    player = Player()
    all_sprites = pygame.sprite.Group()
    ice_blocks = pygame.sprite.Group()

    width, height = screen.get_size()
    total_animals = 20  # total number of animals to rescue
    for _ in range(total_animals):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        ice = IceBlock(x, y)
        ice_blocks.add(ice)
        all_sprites.add(ice)

    all_sprites.add(player)
    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        # Check for collisions with ice blocks (animals)
        for ice in list(ice_blocks):
            if pygame.sprite.collide_rect(player, ice) and not ice.melted:
                ice_blocks.remove(ice)
                all_sprites.remove(ice)
                score += 1
                # Update the held animal to a reduced version.
                player.held_animal = pygame.transform.scale(ice.rescued_image, (50, 50))
                ice.melted = True

        # When all animals have been rescued, end level 1.
        if len(ice_blocks) == 0:
            running = False

        all_sprites.draw(screen)

        if player.current_key_sprite:
            screen.blit(player.current_key_sprite, (10, 55))

        level_text = FONTS["medium"].render("Level: 1", True, BLACK)
        screen.blit(level_text, (10, 10))
        display_score(width, score)

        # Draw the held animal (attached to the player's hand) with an overlay count.
        if player.held_animal:
            held_rect = player.held_animal.get_rect()
            held_rect.center = (player.rect.right - 20, player.rect.centery)
            screen.blit(player.held_animal, held_rect)
            count_text = FONTS["small"].render(str(score), True, BLACK)
            count_rect = count_text.get_rect()
            # Adjust the count text so it appears on the bottom‐right of the held animal.
            count_rect.bottomright = (held_rect.right + count_rect.width // 2, held_rect.bottom - 5)
            screen.blit(count_text, count_rect)

        pygame.display.flip()

    return score

# ------------------------------------------------------------------
# Level 2 Function (Labyrinth)
# ------------------------------------------------------------------

def run_level_two():
    # Local lists for walls and animals.
    walls = []
    animals = []

    # Define labyrinth classes (locally so they don’t conflict with Level 1 classes)
    class LabyrinthPlayer(object):
        def __init__(self):
            self.image = pygame.image.load("assets/muzbek.png")
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()
            self.rect.center = (128, 128)

        def move(self, dx, dy):
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)

        def move_single_axis(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy
            # Check collision with walls
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:  # moving right; hit left side of wall
                        self.rect.right = wall.rect.left
                    if dx < 0:  # moving left; hit right side
                        self.rect.left = wall.rect.right
                    if dy > 0:  # moving down; hit top
                        self.rect.bottom = wall.rect.top
                    if dy < 0:  # moving up; hit bottom
                        self.rect.top = wall.rect.bottom
            # Check collision with trapped animals
            for animal in animals:
                if self.rect.colliderect(animal.rect) and not animal.rescued:
                    animal.rescue()

    class LabyrinthWall(object):
        def __init__(self, pos):
            self.rect = pygame.Rect(pos[0], pos[1], 64, 64)
            walls.append(self)

    class LabyrinthAnimal(object):
        def __init__(self, pos):
            self.image_trapped = pygame.image.load("assets/trapped.png")
            self.image_rescued = pygame.image.load("assets/rescued.png")
            self.image_trapped = pygame.transform.scale(self.image_trapped, (64, 64))
            self.image_rescued = pygame.transform.scale(self.image_rescued, (64, 64))
            self.image = self.image_trapped
            self.rect = self.image.get_rect(topleft=pos)
            self.rescued = False
            animals.append(self)

        def rescue(self):
            self.image = self.image_rescued
            self.rescued = True

    # Level layout: W = wall, E = exit, A = trapped animal.
    level_layout = [
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
    ]

    exit_rect = None
    x = y = 0
    for row in level_layout:
        for col in row:
            if col == "W":
                LabyrinthWall((x, y))
            elif col == "E":
                exit_rect = pygame.Rect(x, y, 64, 64)
            elif col == "A":
                LabyrinthAnimal((x, y))
            x += 64
        y += 64
        x = 0

    player = LabyrinthPlayer()
    clock = pygame.time.Clock()
    labyrinth_running = True

    while labyrinth_running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                labyrinth_running = False

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
        player.move(dx, dy)

        # When the player reaches the exit, end the labyrinth level.
        if exit_rect and player.rect.colliderect(exit_rect):
            labyrinth_running = False

        screen.fill(WHITE)
        # Draw walls.
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall.rect)
        # Draw exit.
        if exit_rect:
            pygame.draw.rect(screen, (255, 0, 0), exit_rect)
        # Draw animals.
        for animal in animals:
            screen.blit(animal.image, animal.rect)
        # Draw the player.
        screen.blit(player.image, player.rect)
        # Display level number.
        level_text = FONTS["medium"].render("Level: 2", True, BLACK)
        screen.blit(level_text, (10, 10))

        pygame.display.flip()

# ------------------------------------------------------------------
# Main Game Runner (Runs Level 1 then Level 2)
# ------------------------------------------------------------------

def run_game(skip_main_menu=False):
    while True:
        if not skip_main_menu and not show_main_menu():
            break
        skip_main_menu = False

        # --- Level 1 ---
        score = run_level_one()
        if not show_win_screen(score, level=1):
            break

        # --- Level 2 (Labyrinth) ---
        run_level_two()
        if not show_win_screen(None, level=2):
            break
        else:
            skip_main_menu = True

if __name__ == "__main__":
    run_game()