# Импорт необходимых библиотек
import pygame  # Основная библиотека для создания игры
import sys     # Для работы с системными функциями (например, выход из игры)
import copy    # Для создания копий объектов
import random  # Для генерации случайных чисел
import time    # Для работы со временем (паузы)
from pygame import gfxdraw  # Для расширенных возможностей рисования

# Инициализация pygame (обязательно в начале)
pygame.init()

# Параметры игры
scale = 15      # Размер одного сегмента змейки и еды
score = 0       # Начальный счет
level = 0       # Начальный уровень
SPEED = 9       # Начальная скорость игры (частота обновления кадров)
SCREEN_WIDTH = 500  # Ширина игрового поля
SCREEN_HEIGHT = 500 # Высота игрового поля

# Настройка экрана
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Создаем окно
pygame.display.set_caption("ЖЫЛАН")  # Устанавливаем заголовок окна
clock = pygame.time.Clock()  # Создаем объект для контроля FPS

# Цвета
background_top = (34, 139, 34)  # Зеленый (верхний фон)
background_bottom = (0, 0, 0)   # Черный (нижний фон)
snake_colour = (139, 69, 19)    # Коричневый (тело змейки)
snake_head = (255, 247, 0)      # Желтый (голова змейки)
font_colour = (255, 255, 255)   # Белый (цвет текста)
defeat_colour = (255, 0, 0)     # Красный (цвет поражения)

class Food:
    """Класс для еды, которую собирает змейка"""
    def __init__(self):
        self.x = 0  # Позиция по X
        self.y = 0  # Позиция по Y
        self.colour = (255, 0, 0)  # Цвет еды
        self.weight = 1  # Вес/очки за еду (обычная еда дает 1-5 очков)
        self.timer = 0  # Таймер до исчезновения еды (в кадрах)
        self.max_timer = 300  # Максимальное время жизни еды (5 сек при 60 FPS)
        self.spawn_time = 0  # Время появления еды
        
    def new_location(self, snake_history):
        """Генерация новой позиции для еды"""
        while True:
            # Случайные координаты в пределах экрана, кратные scale
            self.x = random.randrange(1, int(SCREEN_WIDTH / scale)) * scale
            self.y = random.randrange(1, int(SCREEN_HEIGHT / scale)) * scale
            
            # Проверка на пересечение со змейкой
            overlap = False
            for segment in snake_history:
                if abs(self.x - segment[0]) < scale and abs(self.y - segment[1]) < scale:
                    overlap = True
                    break
            
            if not overlap:  # Если нет пересечения, выходим из цикла
                break
        
        # Определяем тип еды (80% обычная, 15% бонусная, 5% супер бонусная)
        food_type = random.random()
        if food_type < 0.8:
            # Обычная еда (зеленая)
            self.weight = random.randint(1, 5)
            self.colour = (random.randint(50, 200), random.randint(150, 255), random.randint(50, 200))
            self.max_timer = 300  # 5 секунд
        elif food_type < 0.95:
            # Бонусная еда (синяя)
            self.weight = random.randint(5, 10)
            self.colour = (random.randint(50, 150), random.randint(50, 150), random.randint(200, 255))
            self.max_timer = 200  # ~3.3 секунды
        else:
            # Супер бонус (золотая)
            self.weight = random.randint(10, 20)
            self.colour = (255, 215, 0)  # Золотой цвет
            self.max_timer = 150  # 2.5 секунды
            
        self.timer = self.max_timer
        self.spawn_time = pygame.time.get_ticks()  # Запоминаем время появления
    
    def show(self):
        """Отрисовка еды на экране"""
        # Рисуем квадратик еды
        pygame.draw.rect(display, self.colour, (self.x, self.y, scale, scale))
        
        # Рисуем кольцо-таймер (исчезает со временем)
        time_left = self.timer / self.max_timer
        if time_left < 0.3:  # Мигание перед исчезновением
            if pygame.time.get_ticks() % 200 < 100:  # Мигаем каждые 200мс
                return
        
        # Рисуем полупрозрачный круг вокруг еды
        center_x = self.x + scale // 2
        center_y = self.y + scale // 2
        radius = scale // 2 + 3
        
        # Создаем поверхность для полупрозрачного круга
        fade_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        alpha = int(200 * time_left)  # Прозрачность зависит от оставшегося времени
        fade_color = (*self.colour[:3], alpha)  # Цвет с альфа-каналом
        pygame.draw.circle(fade_surface, fade_color, (radius, radius), radius)
        display.blit(fade_surface, (center_x - radius, center_y - radius))
        
        # Показываем вес для бонусной еды
        if self.weight >= 5:
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(self.weight), True, (0, 0, 0))  # Черный текст
            text_rect = text.get_rect(center=(center_x, center_y))
            display.blit(text, text_rect)
    
    def update_timer(self):
        """Обновление таймера еды"""
        if self.timer > 0:
            self.timer -= 1
            return self.timer > 0  # Возвращает True, если время еще есть
        return False

class Snake:
    """Класс змейки"""
    def __init__(self, x_start, y_start):
        self.x = x_start  # Начальная позиция X
        self.y = y_start  # Начальная позиция Y
        self.w = 15       # Ширина сегмента
        self.h = 15       # Высота сегмента
        self.x_dir = 1    # Направление по X (1 - вправо, -1 - влево)
        self.y_dir = 0    # Направление по Y (1 - вниз, -1 - вверх)
        self.history = [[self.x, self.y]]  # История позиций (тело змейки)
        self.length = 1   # Начальная длина

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.x = SCREEN_WIDTH / 2 - scale
        self.y = SCREEN_HEIGHT / 2 - scale
        self.w = 15
        self.h = 15
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        """Отрисовка змейки"""
        for i in range(self.length):
            # Координаты центра текущего сегмента
            center_x = self.history[i][0] + self.w // 2
            center_y = self.history[i][1] + self.h // 2
            # Голова желтая, тело - коричневое
            color = snake_head if i == 0 else snake_colour
            # Рисуем круглый сегмент
            pygame.draw.circle(display, color, (center_x, center_y), self.w // 2)

    def check_eaten(self, food):
        """Проверка, съела ли змейка еду"""
        if abs(self.history[0][0] - food.x) < scale and abs(self.history[0][1] - food.y) < scale:
            return True

    def check_level(self):
        """Проверка на повышение уровня"""
        global level
        if self.length % 5 == 0:  # Уровень повышается каждые 5 съеденных кусочков
            return True

    def grow(self):
        """Увеличение длины змейки"""
        self.length += 1
        # Добавляем новый сегмент в конец (пока просто копируя последний)
        self.history.append(self.history[self.length - 2])

    def death(self):
        """Проверка на столкновение с собой или границами"""
        i = self.length - 1
        while i > 0:
            # Проверка столкновения головы с телом
            if (abs(self.history[0][0] - self.history[i][0]) < self.w and 
                abs(self.history[0][1] - self.history[i][1]) < self.h and 
                self.length > 2):
                return True
            i -= 1

    def update(self):
        """Обновление позиции змейки"""
        # Двигаем каждый сегмент на место предыдущего
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i - 1])
            i -= 1
        # Двигаем голову в текущем направлении
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale

def show_score():
    """Отображение счета"""
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: " + str(score), True, font_colour)
    display.blit(text, (scale, scale))  # Выводим в верхнем левом углу

def show_level():
    """Отображение уровня"""
    font = pygame.font.SysFont(None, 20)
    text = font.render("Level: " + str(level), True, font_colour)
    display.blit(text, (90 - scale, scale))  # Рядом со счетом

def gameLoop():
    """Основной игровой цикл"""
    global score, level, SPEED

    # Создаем змейку по центру экрана
    snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Создаем еду
    food = Food()
    food.new_location(snake.history)
    last_food_time = pygame.time.get_ticks()

    while True:  # Основной цикл игры
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закрытие окна
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Нажатие клавиши
                if event.key == pygame.K_q:  # Клавиша Q - выход
                    pygame.quit()
                    sys.exit()
                # Управление змейкой (нельзя развернуться на 180 градусов)
                if snake.y_dir == 0:  # Если движется по горизонтали
                    if event.key == pygame.K_UP:
                        snake.x_dir = 0
                        snake.y_dir = -1
                    elif event.key == pygame.K_DOWN:
                        snake.x_dir = 0
                        snake.y_dir = 1
                elif snake.x_dir == 0:  # Если движется по вертикали
                    if event.key == pygame.K_LEFT:
                        snake.x_dir = -1
                        snake.y_dir = 0
                    elif event.key == pygame.K_RIGHT:
                        snake.x_dir = 1
                        snake.y_dir = 0

        # Отрисовка фона
        display.fill(background_top)

        # Отрисовка и обновление змейки
        snake.show()
        snake.update()
        
        # Обновление таймера еды и генерация новой при необходимости
        if not food.update_timer():
            food.new_location(snake.history)
            last_food_time = pygame.time.get_ticks()
        
        # Отрисовка еды
        food.show()
        # Показ счета и уровня
        show_score()
        show_level()

        # Проверка, съела ли змейка еду
        if snake.check_eaten(food):
            score += food.weight  # Увеличиваем счет
            food.new_location(snake.history)  # Новая еда
            snake.grow()  # Увеличиваем змейку

        # Проверка на повышение уровня
        if snake.check_level():
            level += 1
            SPEED += 1  # Увеличиваем скорость
            snake.grow()  # Даем бонусный сегмент

        # Проверка на поражение (столкновение или выход за границы)
        if (snake.death() or 
            snake.history[0][0] < 0 or 
            snake.history[0][0] >= SCREEN_WIDTH or 
            snake.history[0][1] < 0 or 
            snake.history[0][1] >= SCREEN_HEIGHT):
            # Сброс параметров игры
            score = 0
            level = 0
            SPEED = 9
            # Сообщение о поражении
            font = pygame.font.SysFont(None, 80)
            text = font.render("ЖЫЛАН ПОГИБ", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)  # Пауза 3 секунды
            # Перезапуск игры
            snake.reset()
            food.new_location(snake.history)

        # Обновление экрана
        pygame.display.update()
        # Контроль FPS (скорости игры)
        clock.tick(SPEED)

# Запуск игры
gameLoop()