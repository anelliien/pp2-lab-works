import pygame, random, sys, time
pygame.init()

# Размеры экрана и блоков
SCREEN_WIDTH, SCREEN_HEIGHT = 620, 400
BLOCK_SIZE = 20  
SPEED = 6  # Начальная скорость
LEVEL_UP_SCORE = 5  # Каждые 5 очков — новый уровень

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Настройки красного шара
RED_FOOD_RADIUS = int(BLOCK_SIZE * 1.5)
BLUE_FOOD_RADIUS = int(BLOCK_SIZE * 0.8)
RED_FOOD_TIME = 8000
RED_FOOD_LIFETIME = 8000

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Шрифт
font = pygame.font.Font(None, 30)

def draw_text(text, x, y, color=WHITE, size=30):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def generate_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLUE_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLUE_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return x, y

def generate_red_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - RED_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - RED_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return {"pos": (x, y), "spawn_time": pygame.time.get_ticks()}

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_position):
    pygame.draw.circle(screen, BLUE, (food_position[0] + BLOCK_SIZE // 2, food_position[1] + BLOCK_SIZE // 2), BLUE_FOOD_RADIUS)

def draw_red_food(red_food):
    pygame.draw.circle(screen, RED, (red_food["pos"][0] + BLOCK_SIZE // 2, red_food["pos"][1] + BLOCK_SIZE // 2), RED_FOOD_RADIUS)
    pygame.draw.circle(screen, BLACK, (red_food["pos"][0] + BLOCK_SIZE // 2, red_food["pos"][1] + BLOCK_SIZE // 2), RED_FOOD_RADIUS, 3)

def draw_timer_bar(time_left):
    bar_width = 200
    bar_height = 10
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 20, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 20, (bar_width * time_left) // RED_FOOD_LIFETIME, bar_height))

def game_over_screen():
    screen.fill(BLACK)
    draw_text("Game Over!", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50, (255, 50, 50), 50)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def game():
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"
    food = generate_food(snake)
    red_food = None
    last_red_food_time = pygame.time.get_ticks()
    score = 0
    level = 1
    speed = SPEED

    blink = True
    blink_timer = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Столкновение с границами
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            game_over_screen()

        # Столкновение с телом
        if (head_x, head_y) in snake:
            game_over_screen()

        snake.insert(0, (head_x, head_y))

        # Поедание синей еды
        if (head_x, head_y) == food:
            score += 1
            food = generate_food(snake)
        else:
            snake.pop()

        # Общая проверка на повышение уровня
        if score // LEVEL_UP_SCORE + 1 > level:
            level += 1
            speed += 0.5

        # Появление красной еды
        if red_food is None and pygame.time.get_ticks() - last_red_food_time > RED_FOOD_TIME:
            red_food = generate_red_food(snake)

        if red_food and pygame.time.get_ticks() - red_food["spawn_time"] > RED_FOOD_LIFETIME:
            red_food = None
            last_red_food_time = pygame.time.get_ticks()

        # Поедание красной еды
        if red_food and (head_x - RED_FOOD_RADIUS <= red_food["pos"][0] <= head_x + RED_FOOD_RADIUS) and \
           (head_y - RED_FOOD_RADIUS <= red_food["pos"][1] <= head_y + RED_FOOD_RADIUS):
            snake.extend(snake[-3:])
            score += 3
            red_food = None
            last_red_food_time = pygame.time.get_ticks()

        # Мигание красной еды
        if pygame.time.get_ticks() - blink_timer > 400:
            blink = not blink
            blink_timer = pygame.time.get_ticks()

        # Отрисовка
        draw_snake(snake)
        draw_food(food)
        if red_food:
            if blink:
                draw_red_food(red_food)
            draw_timer_bar(RED_FOOD_LIFETIME - (pygame.time.get_ticks() - red_food["spawn_time"]))

        draw_text(f"Score: {score}   Level: {level}", 10, 10)

        pygame.display.update()
        clock.tick(speed)

game()
