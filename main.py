# importing libraries
import asyncio
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


# ---------------------------
# FUNCTIONS
# ---------------------------

def show_score(game_window, score):
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"Score : {score}", True, white)
    game_window.blit(score_surface, (10, 10))


def game_over_screen(game_window, score):
    game_window.fill(black)

    big_font = pygame.font.SysFont("times new roman", 60)
    small_font = pygame.font.SysFont("times new roman", 30)

    game_text = big_font.render("GAME OVER", True, red)
    score_text = small_font.render(f"Score: {score}", True, white)

    game_rect = game_text.get_rect(center=(window_x / 2, window_y / 3))
    score_rect = score_text.get_rect(center=(window_x / 2, window_y / 2))

    game_window.blit(game_text, game_rect)
    game_window.blit(score_text, score_rect)

    pygame.display.flip()


def reset_game():
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

    fruit_pos = [
        random.randrange(1, (window_x // 10)) * 10,
        random.randrange(1, (window_y // 10)) * 10
    ]

    direction = "RIGHT"
    change_to = direction
    score = 0

    return snake_pos, snake_body, fruit_pos, direction, change_to, score


# ---------------------------
# MAIN GAME LOOP
# ---------------------------

async def main():

    pygame.init()
    pygame.mixer.init()

    game_window = pygame.display.set_mode((window_x, window_y))
    pygame.display.set_caption("Snake Game")
    fps = pygame.time.Clock()

    # 🔊 Load sounds INSIDE main (important for pygbag)
    crunch_sound = pygame.mixer.Sound("assets/sounds/crunch.ogg")
    die_sound = pygame.mixer.Sound("assets/sounds/die.ogg")

    snake_position, snake_body, fruit_position, direction, change_to, score = reset_game()
    fruit_spawn = True

    running = True

    while running:

        # -----------------
        # EVENTS
        # -----------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"

        # -----------------
        # DIRECTION
        # -----------------
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        elif change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        elif change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        elif change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # -----------------
        # MOVE SNAKE
        # -----------------
        if direction == "UP":
            snake_position[1] -= 10
        elif direction == "DOWN":
            snake_position[1] += 10
        elif direction == "LEFT":
            snake_position[0] -= 10
        elif direction == "RIGHT":
            snake_position[0] += 10

        # -----------------
        # GROWTH / FOOD
        # -----------------
        snake_body.insert(0, list(snake_position))

        if snake_position == fruit_position:
            score += 10
            crunch_sound.play(loops=1)
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [
                random.randrange(1, (window_x // 10)) * 10,
                random.randrange(1, (window_y // 10)) * 10
            ]
            fruit_spawn = True

        # -----------------
        # DRAW
        # -----------------
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(
            game_window,
            red,
            pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
        )

        show_score(game_window, score)

        # -----------------
        # COLLISION
        # -----------------
        collision = (
            snake_position[0] < 0 or snake_position[0] >= window_x or
            snake_position[1] < 0 or snake_position[1] >= window_y
        )

        for block in snake_body[1:]:
            if snake_position == block:
                collision = True

        if collision:
            pygame.time.delay(1000)
            die_sound.play(loops=3)
            
            game_over_screen(game_window, score)
            pygame.display.flip()
            
            pygame.time.delay(2000)

            waiting_for_reset = True

            if waiting_for_reset:
                snake_position, snake_body, fruit_position, direction, change_to, score = reset_game()
                fruit_spawn = True
                waiting_for_reset = False

        # -----------------
        # UPDATE
        # -----------------
        pygame.display.flip()
        fps.tick(snake_speed)

        await asyncio.sleep(0)

asyncio.run(main())