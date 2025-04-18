import pygame, random, sys, time
pygame.init()  # Инициализация всех модулей Pygame

# Размеры экрана и блоков
SCREEN_WIDTH, SCREEN_HEIGHT = 620, 400  # Размер окна игры
BLOCK_SIZE = 20                         # Размер одного блока змейки
SPEED = 6                               # Начальная скорость игры
LEVEL_UP_SCORE = 5                      # Повышение уровня каждые 5 очков

# Цвета (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)     # Цвет змейки
RED = (255, 0, 0)       # Цвет красной еды
BLUE = (0, 0, 255)      # Цвет синей еды
BLACK = (0, 0, 0)

# Настройки красной еды
RED_FOOD_RADIUS = int(BLOCK_SIZE * 1.5)   # Радиус красной еды
BLUE_FOOD_RADIUS = int(BLOCK_SIZE * 0.8)  # Радиус синей еды
RED_FOOD_TIME = 8000       # Задержка перед появлением красной еды (в мс)
RED_FOOD_LIFETIME = 8000   # Время жизни красной еды (в мс)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")  # Заголовок окна

# Шрифт для текста
font = pygame.font.Font(None, 30)

# Функция отрисовки текста
def draw_text(text, x, y, color=WHITE, size=30):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Функция генерации синей еды
def generate_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLUE_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLUE_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return x, y

# Функция генерации красной еды
def generate_red_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - RED_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - RED_FOOD_RADIUS * 2) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return {"pos": (x, y), "spawn_time": pygame.time.get_ticks()}  # сохраняем время появления

# Отрисовка змейки
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Отрисовка синей еды
def draw_food(food_position):
    pygame.draw.circle(screen, BLUE, (food_position[0] + BLOCK_SIZE // 2, food_position[1] + BLOCK_SIZE // 2), BLUE_FOOD_RADIUS)

# Отрисовка красной еды с обводкой
def draw_red_food(red_food):
    pygame.draw.circle(screen, RED, (red_food["pos"][0] + BLOCK_SIZE // 2, red_food["pos"][1] + BLOCK_SIZE // 2), RED_FOOD_RADIUS)
    pygame.draw.circle(screen, BLACK, (red_food["pos"][0] + BLOCK_SIZE // 2, red_food["pos"][1] + BLOCK_SIZE // 2), RED_FOOD_RADIUS, 3)

# Таймер снизу под красной едой
def draw_timer_bar(time_left):
    bar_width = 200
    bar_height = 10
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 20, bar_width, bar_height))  # фон
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - bar_width // 2, SCREEN_HEIGHT - 20, (bar_width * time_left) // RED_FOOD_LIFETIME, bar_height))  # заполнение

# Экран окончания игры
def game_over_screen():
    screen.fill(BLACK)
    draw_text("Game Over!", SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50, (255, 50, 50), 50)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Основная функция игры
def game():
    snake = [(100, 100), (90, 100), (80, 100)]  # Начальное тело змейки
    direction = "RIGHT"                         # Начальное направление
    food = generate_food(snake)                # Синяя еда
    red_food = None
    last_red_food_time = pygame.time.get_ticks()
    score = 0
    level = 1
    speed = SPEED

    blink = True               # Флаг мигания
    blink_timer = pygame.time.get_ticks()  # Таймер мигания

    clock = pygame.time.Clock()  # Контроль FPS

    while True:
        screen.fill(BLACK)  # Очистка экрана

        # Обработка событий клавиатуры
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

        # Движение головы змейки
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Проверка выхода за границы
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            game_over_screen()

        # Проверка столкновения с телом
        if (head_x, head_y) in snake:
            game_over_screen()

        snake.insert(0, (head_x, head_y))  # Добавляем новую голову

        # Проверка поедания синей еды
        if (head_x, head_y) == food:
            score += 1
            food = generate_food(snake)
        else:
            snake.pop()  # Удаляем последний сегмент (движение)

        # Проверка повышения уровня
        if score // LEVEL_UP_SCORE + 1 > level:
            level += 1
            speed += 0.5  # Увеличение скорости

        # Появление красной еды
        if red_food is None and pygame.time.get_ticks() - last_red_food_time > RED_FOOD_TIME:
            red_food = generate_red_food(snake)

        # Красная еда исчезает, если время вышло
        if red_food and pygame.time.get_ticks() - red_food["spawn_time"] > RED_FOOD_LIFETIME:
            red_food = None
            last_red_food_time = pygame.time.get_ticks()

        # Съедание красной еды (учитываем радиус)
        if red_food and (head_x - RED_FOOD_RADIUS <= red_food["pos"][0] <= head_x + RED_FOOD_RADIUS) and \
           (head_y - RED_FOOD_RADIUS <= red_food["pos"][1] <= head_y + RED_FOOD_RADIUS):
            snake.extend(snake[-3:])  # Удлинить змейку на 3 блока
            score += 3
            red_food = None
            last_red_food_time = pygame.time.get_ticks()

        # Мигание красной еды
        if pygame.time.get_ticks() - blink_timer > 400:
            blink = not blink
            blink_timer = pygame.time.get_ticks()

        # Отрисовка объектов
        draw_snake(snake)
        draw_food(food)
        if red_food:
            if blink:
                draw_red_food(red_food)
            draw_timer_bar(RED_FOOD_LIFETIME - (pygame.time.get_ticks() - red_food["spawn_time"]))

        draw_text(f"Score: {score}   Level: {level}", 10, 10)

        pygame.display.update()
        clock.tick(speed)  # Задержка, зависит от скорости

# Запуск игры
game()
