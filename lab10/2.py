import pygame
import random
import sys
import psycopg2

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

conn = psycopg2.connect(
    dbname='suppliers',
    user='postgres',
    password='anelliien',
    host='localhost'
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(255) UNIQUE
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        score INTEGER,
        level INTEGER
    );
""")
conn.commit()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GRAY  = (100, 100, 100)

MAX_LEVEL = 10

def get_or_create_user(username):
    cursor.execute("SELECT user_id FROM users WHERE user_name = %s;", (username,))
    row = cursor.fetchone()
    if row:
        user_id = row[0]
        cursor.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1;", (user_id,))
        level_row = cursor.fetchone()
        return user_id, level_row[0] if level_row else 1
    else:
        cursor.execute("INSERT INTO users (user_name) VALUES (%s) RETURNING user_id;", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id, 1

def save_score(user_id, score, level):
    cursor.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s);", (user_id, score, level))
    conn.commit()

def generate_level_walls(level):
    new_walls = []
    if level == 2:
        new_walls += [(i, GRID_HEIGHT // 2) for i in range(5, GRID_WIDTH - 5)]
    elif level == 3:
        new_walls += [(GRID_WIDTH // 2, i) for i in range(5, GRID_HEIGHT - 5)]
    elif level >= 4:
        for i in range(5, GRID_WIDTH - 5, 4):
            new_walls += [(i, i % GRID_HEIGHT)]
    return new_walls

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.paused = False

    def get_player_name(self):
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = input_box.collidepoint(event.pos)
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN and text.strip():
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill(BLACK)
            title_font = pygame.font.SysFont(None, 40)
            title_surface = title_font.render("Enter your username:", True, WHITE)
            screen.blit(title_surface, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60))

            txt_surface = font.render(text, True, color)
            input_box.w = max(200, txt_surface.get_width() + 10)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()

        self.player_name = text
        self.user_id, loaded_level = get_or_create_user(self.player_name)
        return loaded_level

    def move(self):
        global score, level, speed, walls, food
        if self.paused:
            return True

        head = self.body[0]
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH,
                    (head[1] + self.direction[1]) % GRID_HEIGHT)

        if new_head in self.body[1:] or new_head in walls:
            return False

        self.body.insert(0, new_head)
        if new_head == food.position:
            score += 1
            if score % 3 == 0 and level < MAX_LEVEL:
                level += 1
                speed += 0.5  # медленнее нарастает
                walls += generate_level_walls(level)
            food.spawn()
        else:
            self.body.pop()
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def save_progress(self):
        save_score(self.user_id, score, level)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        while True:
            pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
            if pos not in snake.body and pos not in walls:
                self.position = pos
                break

def draw_game():
    screen.fill(BLACK)
    for segment in snake.body:
        pygame.draw.rect(screen, WHITE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for wall in walls:
        pygame.draw.rect(screen, GRAY, (wall[0] * GRID_SIZE, wall[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    # Кнопка Pause/Resume
    global pause_button_rect
    pause_button_rect = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 30)
    pygame.draw.rect(screen, GRAY, pause_button_rect)
    pause_text = font.render("Resume" if snake.paused else "Pause", True, WHITE)
    screen.blit(pause_text, (pause_button_rect.x + 10, pause_button_rect.y + 5))

    if snake.paused:
        pause_text_overlay = font.render("PAUSED - press SPACE or P", True, WHITE)
        screen.blit(pause_text_overlay, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2))

    pygame.display.flip()

def reset_game():
    global score, level, speed, walls, food
    snake.reset()
    score = 0
    level = loaded_level
    speed = 5 + (level - 1) * 0.5  # уменьшена начальная скорость
    walls = [(0, i) for i in range(GRID_HEIGHT)] + [(GRID_WIDTH - 1, i) for i in range(GRID_HEIGHT)] + \
            [(i, 0) for i in range(GRID_WIDTH)] + [(i, GRID_HEIGHT - 1) for i in range(GRID_WIDTH)]
    walls += generate_level_walls(level)
    food = Food()

# --- Game setup ---
snake = Snake()
loaded_level = snake.get_player_name()
reset_game()

clock = pygame.time.Clock()
running = True
game_over = False

while running:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake.save_progress()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
                elif event.key == pygame.K_SPACE:
                    snake.paused = not snake.paused
                elif event.key == pygame.K_p:
                    game_over = True
                elif event.key == pygame.K_s:
                    snake.save_progress()

        if not snake.move():
            game_over = True

        draw_game()
        clock.tick(speed)
       
    else:
        screen.fill(BLACK)
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 36)

        # GAME OVER текст
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(game_over_text, game_over_rect)

        # Кнопка Restart
        restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50)
        pygame.draw.rect(screen, GRAY, restart_rect)
        restart_text = font_medium.render("Restart", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        screen.blit(restart_text, restart_text_rect)

        # Кнопка Exit
        exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(screen, GRAY, exit_rect)
        exit_text = font_medium.render("Exit", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    snake.paused = not snake.paused
                elif exit_rect.collidepoint(event.pos):
                    running = False
                elif restart_rect.collidepoint(event.pos):
                        snake.save_progress()
                        reset_game()
                        game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    snake.save_progress()
                    reset_game()
                    game_over = False
                elif event.key == pygame.K_SPACE:
                    running = False
                elif event.key == pygame.K_p:
                    running = False
pygame.quit()
conn.close()