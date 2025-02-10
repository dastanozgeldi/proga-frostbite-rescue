import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Heat Ray Rescue")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load images
try:
    player = pygame.image.load("assets/muzbek.png")
    frozen_animal = pygame.image.load("assets/trapped.png")
    rescued_animal = pygame.image.load("assets/rescued.png")
except pygame.error:
    # Fallback rectangles if images aren't found
    player = pygame.Surface((50, 50))
    player.fill(YELLOW)
    frozen_animal = pygame.Surface((60, 60))
    frozen_animal.fill(WHITE)
    rescued_animal = pygame.Surface((60, 60))
    rescued_animal.fill(RED)

# Scale images
PLAYER_SIZE = (50, 50)
ANIMAL_SIZE = (60, 60)
player = pygame.transform.scale(player, PLAYER_SIZE)
frozen_animal = pygame.transform.scale(frozen_animal, ANIMAL_SIZE)
rescued_animal = pygame.transform.scale(rescued_animal, ANIMAL_SIZE)

# Game variables
player_pos = [WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2]
THAW_RATE = 0.5
REQUIRED_THAW = 100
NUM_ANIMALS = 5

# Create list of animals with random positions
animals = []
for _ in range(NUM_ANIMALS):
    # Ensure animals don't spawn too close to edges
    x = random.randint(ANIMAL_SIZE[0], WINDOW_WIDTH - ANIMAL_SIZE[0])
    y = random.randint(ANIMAL_SIZE[1], WINDOW_HEIGHT - ANIMAL_SIZE[1])
    
    animals.append({
        'pos': [x, y],
        'thaw_progress': 0,
        'rescued': False
    })

# Game loop
clock = pygame.time.Clock()
running = True
animals_rescued = 0

def draw_heat_ray(start_pos, end_pos):
    pygame.draw.line(screen, RED, start_pos, end_pos, 2)

    for i in range(1, 3):
        alpha_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(alpha_surface, (255, 0, 0, 50 - i * 20), 
                        start_pos, end_pos, 4 + i * 2)
        screen.blit(alpha_surface, (0, 0))

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos[1] = max(0, player_pos[1] - 5)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos[1] = min(WINDOW_HEIGHT - PLAYER_SIZE[1], player_pos[1] + 5)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos[0] = max(0, player_pos[0] - 5)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos[0] = min(WINDOW_WIDTH - PLAYER_SIZE[0], player_pos[0] + 5)

    # Get mouse position for heat ray
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    # Update thaw progress if heat ray is active
    if mouse_buttons[0]:  # Left mouse button
        for animal in animals:
            if not animal['rescued']:
                # Calculate distance between ray and animal
                distance = math.sqrt(
                    (mouse_pos[0] - (animal['pos'][0] + ANIMAL_SIZE[0]/2))**2 +
                    (mouse_pos[1] - (animal['pos'][1] + ANIMAL_SIZE[1]/2))**2
                )
                
                if distance < 50:  # Heat ray effective range
                    animal['thaw_progress'] = min(REQUIRED_THAW, 
                                                animal['thaw_progress'] + THAW_RATE)
                    if animal['thaw_progress'] >= REQUIRED_THAW:
                        animal['rescued'] = True
                        animals_rescued += 1

    # Clear screen
    screen.fill((0, 0, 100))  # Dark blue background

    # Draw player
    screen.blit(player, player_pos)

    # Draw animals
    for animal in animals:
        if animal['rescued']:
            screen.blit(rescued_animal, animal['pos'])
        else:
            screen.blit(frozen_animal, animal['pos'])
            # Draw thaw progress bar
            pygame.draw.rect(screen, WHITE, 
                           (animal['pos'][0], animal['pos'][1] - 20, 
                            ANIMAL_SIZE[0], 10), 1)
            pygame.draw.rect(screen, RED,
                           (animal['pos'][0], animal['pos'][1] - 20, 
                            ANIMAL_SIZE[0] * (animal['thaw_progress'] / REQUIRED_THAW), 10))

    # Draw heat ray if active
    if mouse_buttons[0]:
        draw_heat_ray((player_pos[0] + PLAYER_SIZE[0]/2, 
                      player_pos[1] + PLAYER_SIZE[1]/2), mouse_pos)

    # Draw rescue counter
    font = pygame.font.Font(None, 36)
    text = font.render(f'Animals Rescued: {animals_rescued}/{NUM_ANIMALS}', True, WHITE)
    screen.blit(text, (10, 10))

    # Check for win condition
    if animals_rescued == NUM_ANIMALS:
        win_text = font.render('All Animals Rescued!', True, YELLOW)
        text_rect = win_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        screen.blit(win_text, text_rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()