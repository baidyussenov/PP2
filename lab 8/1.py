# Импорт необходимых модулей
import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Настройка FPS (кадров в секунду)
FPS = 60
FramePerSec = pygame.time.Clock()

# Определение цветов (RGB)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Основные переменные игры
SCREEN_WIDTH = 400     # Ширина окна
SCREEN_HEIGHT = 800    # Высота окна
SPEED = 5              # Начальная скорость объектов (враги и монеты)
SCORE = 0              # Очки за избегание врагов
COINS = 0              # Счётчик собранных монет

# Настройка шрифтов
font = pygame.font.SysFont("Times New Roman", 30)
font_small = pygame.font.SysFont("Times New Roman", 20)

# Сообщение "Game Over", разбитое на 2 строки
game_over1 = font.render("НЕ шашкуй, брат!", True, WHITE)
game_over2 = font.render("Дома мать ждет!", True, WHITE)

# Загрузка фонового изображения
background = pygame.image.load("lab 8/elements/AnimatedStreet1.png")

# Создание окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Car Dodge Game")

# ---------- Класс Игрока ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка изображения машины игрока
        self.image = pygame.image.load("lab 8/elements/Player1.png")
        self.rect = self.image.get_rect()  # Получение прямоугольника (границы) объекта
        self.rect.center = (160, 520)      # Начальная позиция игрока

    def move(self):
        # Получаем список нажатых клавиш
        pressed_keys = pygame.key.get_pressed()

        # Движение влево (если не выходит за границу экрана)
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-8, 0)

        # Движение вправо
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(8, 0)

# ---------- Класс Вражеской Машины ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/elements/Enemy.png")
        self.rect = self.image.get_rect()
        # Враг появляется в случайной горизонтальной позиции сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        # Движение врага вниз по экрану
        self.rect.move_ip(0, SPEED)
        # Если враг вышел за нижнюю границу — начисляем очко и сбрасываем его вверх
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# ---------- Класс Монеты ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lab 8/elements/Coin.png")
        # Изменяем размер монеты (по желанию)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        # Монета появляется в случайной позиции сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Монета движется вниз
        self.rect.move_ip(0, SPEED)
        # Если монета вышла за экран — появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Создание экземпляров объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие для увеличения скорости (каждую секунду)
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# ---------- Главный Игровой Цикл ----------
while True:
    for event in pygame.event.get():
        # Увеличиваем скорость каждую секунду
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Выход из игры
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение счёта и количества монет
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Отображение и обновление всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка на столкновение игрока с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        # Воспроизведение звука удара
        pygame.mixer.Sound("lab 8/elements/crash.wav").play()
        time.sleep(0.5)

        # Показываем красный экран с сообщением "Game Over"
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over1, (60, 250))
        DISPLAYSURF.blit(game_over2, (60, 290))
        pygame.display.update()
        time.sleep(2)

        # Удаляем все объекты
        for entity in all_sprites:
            entity.kill()

        # Завершаем игру
        pygame.quit()
        sys.exit()

    # Проверка на сбор монеты
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        # Переместить монету наверх и в новое случайное место
        for coin in coins:
            coin.rect.top = 0
            coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # Обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)
