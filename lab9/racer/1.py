import pygame, sys, random, time
from pygame.locals import *

pygame.init()

# Частота кадров
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

# Параметры экрана и игры
SCREEN_WIDTH = 405
SCREEN_HEIGHT = 600
SPEED = 5 
SCORE = 0  
COINS = 0  

# Шрифты
font = pygame.font.SysFont("Verdana", 60)  
font_small = pygame.font.SysFont("Verdana", 20)  
game_over = font.render("Game Over", True, BLACK)  

# Фон
background = pygame.image.load("image/animated_street.png")

# Окно игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race")

# Звуки
pygame.mixer.music.load("image/background.wav")
pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound("image/winning_a_coin.wav")
crash_sound = pygame.mixer.Sound("image/crash.wav")

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("image/enemy.png")  
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс монеты с разной ценностью
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Случайно выбираем монету
        coin_type = random.choice([(1, "coin1.png"), (3, "coin3.png"), (5, "coin5.png")])
        self.value = coin_type[0]
        self.image = pygame.image.load("image/" + coin_type[1])
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("image/player.png")  
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Фон
    DISPLAYSURF.blit(background, (0, 0))

    # Счёт и монеты
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))  
    DISPLAYSURF.blit(coin_text, (300, 10))  

    # Отрисовка и движение
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        crash_sound.play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Столкновение с монетой
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        COINS += collected_coin.value  # добавляем значение монеты
        coin_sound.play()
        collected_coin.kill()

        # Увеличиваем скорость каждые 10 монет
        if COINS % 10 == 0:
            SPEED += 1

        # Новая монета
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    pygame.display.update()
    FramePerSec.tick(FPS)
