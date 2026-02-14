# importing libraries
import pygame
import random

# Game settings
snake_speed = 15
window_x = 720
window_y = 480

# Define colours
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Initialise Pygame
pygame.init()
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Snake initial position and body
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Fruit initial position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True

# Initial direction
direction = 'RIGHT'
change_to = direction

# Initial score
score = 0

# ---------------------------
# FUNCTIONS
# ---------------------------

def show_score():
    # Display the current score on the screen
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score : {score}', True, white)
    game_window.blit(score_surface, (10, 10))


def game_over():
    # Show game over screen and quit
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render(f'Your Score : {score}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # pause 2 seconds
    pygame.quit()
    quit()


# ---------------------------
# MAIN GAME LOOP
# ---------------------------

while True:
    # Event handling (keyboard input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Update direction (prevent snake from moving opposite to itself)
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # Spawn new fruit
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

    # Fill game window
    game_window.fill(black)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Check for collisions with walls
    if snake_position[0] < 0 or snake_position[0] >= window_x:
        game_over()
    if snake_position[1] < 0 or snake_position[1] >= window_y:
        game_over()

    # Check for collisions with self
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Display score
    show_score()

    # Refresh screen
    pygame.display.update()

    # Control snake speed
    fps.tick(snake_speed)