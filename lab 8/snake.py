import pygame  
import sys  
import copy  
import random  
import time  

pygame.init()

# Устанавливаем параметры игры
scale = 15
score = 0
level = 0
SPEED = 9
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Координаты еды
food_x = 10
food_y = 10

# Создаем окно
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ЖЫЛАН")
clock = pygame.time.Clock()

# Цвета
background_top = (34, 139, 34)
background_bottom = (0, 0, 0)
snake_colour = (139, 69, 19)
food_colour = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
snake_head = (255, 247, 0)
font_colour = (255, 255, 255)
defeat_colour = (255, 0, 0)

# Класс змейки
class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.w = 15
        self.h = 15
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def reset(self):
        self.x = SCREEN_WIDTH / 2 - scale
        self.y = SCREEN_HEIGHT / 2 - scale
        self.w = 15
        self.h = 15
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x, self.y]]
        self.length = 1

    def show(self):
        for i in range(self.length):
            center_x = self.history[i][0] + self.w // 2
            center_y = self.history[i][1] + self.h // 2
            color = snake_head if i == 0 else snake_colour
            pygame.draw.circle(display, color, (center_x, center_y), self.w // 2)

    def check_eaten(self):
        if abs(self.history[0][0] - food_x) < scale and abs(self.history[0][1] - food_y) < scale:
            return True

    def check_level(self):
        global level
        if self.length % 5 == 0:
            return True

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True
            i -= 1

    def update(self):
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i - 1])
            i -= 1
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale

# Класс еды
class Food:
    def new_location(self, snake_history):
        global food_x, food_y, food_colour
        while True:
            food_x = random.randrange(1, int(SCREEN_WIDTH / scale) - 1) * scale
            food_y = random.randrange(1, int(SCREEN_HEIGHT / scale) - 1) * scale
            overlap = False
            for segment in snake_history:
                if abs(food_x - segment[0]) < scale and abs(food_y - segment[1]) < scale:
                    overlap = True
                    break
            if not overlap:
                break
        food_colour = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

    def show(self):
        pygame.draw.rect(display, food_colour, (food_x, food_y, scale, scale))

# Функции отображения счёта и уровня
def show_score():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: " + str(score), True, font_colour)
    display.blit(text, (scale, scale))

def show_level():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Level: " + str(level), True, font_colour)
    display.blit(text, (90 - scale, scale))

# Главный игровой цикл
def gameLoop():
    global score, level, SPEED

    snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    food = Food()
    food.new_location(snake.history)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if snake.y_dir == 0:
                    if event.key == pygame.K_UP:
                        snake.x_dir = 0
                        snake.y_dir = -1
                    elif event.key == pygame.K_DOWN:
                        snake.x_dir = 0
                        snake.y_dir = 1
                elif snake.x_dir == 0:
                    if event.key == pygame.K_LEFT:
                        snake.x_dir = -1
                        snake.y_dir = 0
                    elif event.key == pygame.K_RIGHT:
                        snake.x_dir = 1
                        snake.y_dir = 0

        display.fill(background_top)

        snake.show()
        snake.update()
        food.show()
        show_score()
        show_level()

        if snake.check_eaten():
            food.new_location(snake.history)
            score += random.randint(1, 5)
            snake.grow()

        if snake.check_level():
            food.new_location(snake.history)
            level += 1
            SPEED += 1
            snake.grow()

        if snake.death():
            score = 0
            level = 0
            font = pygame.font.SysFont(None, 80)
            text = font.render("ЖЫЛАН ПОГИБ", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)
            snake.reset()

        # Проверка на столкновение со стенами
        if (snake.history[0][0] < 0 or 
            snake.history[0][0] >= SCREEN_WIDTH or 
            snake.history[0][1] < 0 or 
            snake.history[0][1] >= SCREEN_HEIGHT):
            score = 0
            level = 0
            font = pygame.font.SysFont(None, 80)
            text = font.render("ЖЫЛАН ПОГИБ", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)
            snake.reset()

        pygame.display.update()
        clock.tick(SPEED)

gameLoop()
