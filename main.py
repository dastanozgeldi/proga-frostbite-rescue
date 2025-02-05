import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FONTS = {
    "title": pygame.font.Font(None, 120),
    "button": pygame.font.Font(None, 60),
    "score": pygame.font.Font(None, 50),
}

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Frostbite Rescue")


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


def show_win_screen(score):
    screen.fill(WHITE)

    text = FONTS["title"].render("You Won!", True, BLACK)
    text_rect = text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 3)
    )

    score_text = FONTS["score"].render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (screen.get_width() - 180, 10))

    play_again_text = FONTS["button"].render("Play Again", True, BLACK)
    play_again_rect = play_again_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )

    quit_text = FONTS["button"].render("Quit", True, BLACK)
    quit_rect = quit_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 100)
    )

    screen.blit(text, text_rect)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return True
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    return False


def run_game(skip_main_menu=False):
    while True:
        if not skip_main_menu and not show_main_menu():
            break

        skip_main_menu = False

        player = Player()
        all_sprites = pygame.sprite.Group()
        ice_blocks = pygame.sprite.Group()

        width, height = screen.get_size()
        for _ in range(20):
            ice = IceBlock(
                random.randint(100, width - 100), random.randint(100, height - 100)
            )
            ice_blocks.add(ice)
            all_sprites.add(ice)

        all_sprites.add(player)

        clock = pygame.time.Clock()
        running = True
        score = 0

        while running:
            clock.tick(FPS)
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            player.update(keys)

            for ice in ice_blocks:
                if pygame.sprite.collide_rect(player, ice):
                    score += ice.melt()

            if all(ice.melted for ice in ice_blocks):
                running = False

            all_sprites.draw(screen)

            if player.current_key_sprite:
                screen.blit(player.current_key_sprite, (10, 10))

            score_text = FONTS["score"].render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (screen.get_width() - 180, 10))

            pygame.display.flip()

        if not show_win_screen(score):
            break
        else:
            skip_main_menu = True


if __name__ == "__main__":
    run_game()
