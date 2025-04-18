import pygame, sys, random, time
from pygame.locals import *

# Инициализация всех модулей Pygame
pygame.init()

# Частота кадров в секунду
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета (RGB)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# Параметры экрана и переменные игры
SCREEN_WIDTH = 405
SCREEN_HEIGHT = 600
SPEED = 5           # Начальная скорость
SCORE = 0           # Счёт за объезженных врагов
COINS = 0           # Количество собранных монет

# Шрифты для надписей
font = pygame.font.SysFont("Verdana", 60)  
font_small = pygame.font.SysFont("Verdana", 20)  
game_over = font.render("Game Over", True, BLACK)  # Текст при окончании игры

# Фон игры
background = pygame.image.load("image/animated_street.png")

# Создание окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race")  # Заголовок окна

# Музыка и звуки
pygame.mixer.music.load("image/background.wav")  # Фоновая музыка
pygame.mixer.music.play(-1)  # Воспроизводить бесконечно

coin_sound = pygame.mixer.Sound("image/winning_a_coin.wav")  # Звук монеты
crash_sound = pygame.mixer.Sound("image/crash.wav")          # Звук аварии

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("image/enemy.png")  # Картинка врага
        self.rect = self.image.get_rect()
        # Случайное начальное положение по горизонтали
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Двигаться вниз со скоростью SPEED
        if self.rect.top > SCREEN_HEIGHT:  # Если вышел за экран
            SCORE += 1                     # Увеличить счёт
            self.rect.top = 0             # Вернуть наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс монеты с разной ценностью
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Случайно выбираем тип монеты (ценность и изображение)
        coin_type = random.choice([(1, "coin1.png"), (3, "coin3.png"), (5, "coin5.png")])
        self.value = coin_type[0]
        self.image = pygame.image.load("image/" + coin_type[1])
        self.image = pygame.transform.scale(self.image, (30, 30))  # Масштабируем изображение
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)  # Двигаться вниз
        if self.rect.top > SCREEN_HEIGHT:  # Если вышла за экран — переместить наверх
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("image/player.png")  # Машина игрока
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальное положение внизу экрана

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Проверяем нажатия
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)  # Движение влево
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)   # Движение вправо

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы для упрощения обработки объектов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отображаем фон
    DISPLAYSURF.blit(background, (0, 0))

    # Выводим счёт и количество монет
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))  
    DISPLAYSURF.blit(coin_text, (300, 10))  

    # Отрисовка всех объектов и их движение
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()  # Воспроизвести звук аварии
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)  # Покрасить экран в красный
        DISPLAYSURF.blit(game_over, (30, 250))  # Показать надпись "Game Over"
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Удалить все объекты
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка столкновения с монетой
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        COINS += collected_coin.value  # Добавить значение монеты к общему количеству
        coin_sound.play()              # Звук сбора монеты
        collected_coin.kill()          # Удалить собранную монету

        # Каждые 10 монет увеличиваем скорость
        if COINS % 10 == 0:
            SPEED += 1

        # Создать новую монету
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)  # Поддерживаем заданную частоту кадров
