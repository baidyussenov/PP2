# Импортируем нужные модули
import pygame, sys
from pygame.locals import *
import random, time

# Инициализируем Pygame и загружаем фоновую музыку
pygame.init()
pygame.mixer.music.load("lab 8/elements/background.wav")
pygame.mixer.music.set_volume(0.3)     # Устанавливаем громкость
pygame.mixer.music.play(-1)            # Бесконечное воспроизведение

# Настройка FPS (кадров в секунду)
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета (RGB)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры экрана и начальные переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 5                      # Начальная скорость врагов и монет
SCORE = 0                      # Очки за уверенное вождение
TOTAL_COIN_WEIGHT = 0         # Общий "вес" всех собранных монет

# Шрифты
font = pygame.font.SysFont("Times New Roman", 30)
font_small = pygame.font.SysFont("Times New Roman", 20)

# Сообщения при окончании игры
game_over1 = font.render("НЕ шашкуй, брат!", True, WHITE)
game_over2 = font.render("Дома мать ждет!", True, WHITE)

# Загружаем фоновую картинку дороги
background = pygame.image.load("lab 8/elements/AnimatedStreet1.png")

# Создаем окно игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Car Dodge Game")

# ---------------- Класс игрока (машина игрока) ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/elements/Player1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция на экране

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Проверяем нажатые клавиши
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)  # Двигаем влево
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(8, 0)   # Двигаем вправо

# ---------------- Класс врага ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/elements/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Двигаем врага вниз
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  # Если враг "уехал вниз", даём игроку очко
            self.rect.top = 0  # Сбрасываем врага наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# ---------------- Класс монеты ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/elements/Coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))  # Размер монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 2, 3])  # Случайный "вес" монеты

    def move(self):
        self.rect.move_ip(0, SPEED)  # Монета двигается вниз
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()  # Если уехала вниз — сброс

    def reset(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = random.choice([1, 2, 3])  # Новый вес при каждом появлении

# Создаём объекты игрока, врага и монеты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы объектов (для удобной обработки)
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Создаем пользовательское событие: увеличивать скорость каждую секунду
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Каждые 1000 мс (1 секунда)

# ---------------- Главный игровой цикл ----------------
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Постепенно увеличиваем общую скорость
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Рисуем фон
    DISPLAYSURF.blit(background, (0, 0))

    # Показываем текущий счёт и "вес" монет
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(TOTAL_COIN_WEIGHT), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Обрабатываем все спрайты: рисуем и двигаем
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверяем столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("lab 8/elements/crash.wav").play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over1, (60, 250))
        DISPLAYSURF.blit(game_over2, (60, 290))
        pygame.display.update()
        time.sleep(2)
        for entity in all_sprites:
            entity.kill()
        pygame.quit()
        sys.exit()

    # Проверяем сбор монеты
    if pygame.sprite.spritecollideany(P1, coins):
        for coin in coins:
            TOTAL_COIN_WEIGHT += coin.weight  # Прибавляем вес монеты
            coin.reset()  # Сбрасываем монету на новое место

        # Увеличиваем скорость, если набрано кратно 10 веса
        if TOTAL_COIN_WEIGHT % 10 == 0:
            SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)  # Ограничение FPS
