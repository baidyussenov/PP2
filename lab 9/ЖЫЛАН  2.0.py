import pygame
import sys
import copy
import random
import time
from pygame import gfxdraw

pygame.init()

# Game parameters
scale = 15
score = 0
level = 0
SPEED = 9
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Screen setup
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ЖЫЛАН")
clock = pygame.time.Clock()

# Colors
background_top = (34, 139, 34)
background_bottom = (0, 0, 0)
snake_colour = (139, 69, 19)
snake_head = (255, 247, 0)
font_colour = (255, 255, 255)
defeat_colour = (255, 0, 0)

class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.colour = (255, 0, 0)
        self.weight = 1  # Regular food gives 1-5 points
        self.timer = 0  # Time before food disappears (in frames)
        self.max_timer = 300  # 5 seconds at 60 FPS
        self.spawn_time = 0
        
    def new_location(self, snake_history):
        while True:
            self.x = random.randrange(1, int(SCREEN_WIDTH / scale)) * scale
            self.y = random.randrange(1, int(SCREEN_HEIGHT / scale)) * scale
            
            # Check for overlap with snake
            overlap = False
            for segment in snake_history:
                if abs(self.x - segment[0]) < scale and abs(self.y - segment[1]) < scale:
                    overlap = True
                    break
            
            if not overlap:
                break
        
        # Randomly determine food type (80% normal, 15% bonus, 5% super bonus)
        food_type = random.random()
        if food_type < 0.8:
            # Normal food (green)
            self.weight = random.randint(1, 5)
            self.colour = (random.randint(50, 200), random.randint(150, 255), random.randint(50, 200))
            self.max_timer = 300  # 5 seconds
        elif food_type < 0.95:
            # Bonus food (blue)
            self.weight = random.randint(5, 10)
            self.colour = (random.randint(50, 150), random.randint(50, 150), random.randint(200, 255))
            self.max_timer = 200  # ~3.3 seconds
        else:
            # Super bonus (gold)
            self.weight = random.randint(10, 20)
            self.colour = (255, 215, 0)
            self.max_timer = 150  # 2.5 seconds
            
        self.timer = self.max_timer
        self.spawn_time = pygame.time.get_ticks()
    
    def show(self):
        # Draw food
        pygame.draw.rect(display, self.colour, (self.x, self.y, scale, scale))
        
        # Draw timer ring (fading based on remaining time)
        time_left = self.timer / self.max_timer
        if time_left < 0.3:  # Blink when about to disappear
            if pygame.time.get_ticks() % 200 < 100:  # Blink every 200ms
                return
        
        # Draw a fading circle around the food
        center_x = self.x + scale // 2
        center_y = self.y + scale // 2
        radius = scale // 2 + 3
        
        # Create a surface for the fading circle
        fade_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        alpha = int(200 * time_left)
        fade_color = (*self.colour[:3], alpha)
        pygame.draw.circle(fade_surface, fade_color, (radius, radius), radius)
        display.blit(fade_surface, (center_x - radius, center_y - radius))
        
        # Draw weight indicator for bonus foods
        if self.weight >= 5:
            font = pygame.font.SysFont(None, 20)
            text = font.render(str(self.weight), True, (0, 0, 0))
            text_rect = text.get_rect(center=(center_x, center_y))
            display.blit(text, text_rect)
    
    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
            return self.timer > 0
        return False

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

    def check_eaten(self, food):
        if abs(self.history[0][0] - food.x) < scale and abs(self.history[0][1] - food.y) < scale:
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

def show_score():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: " + str(score), True, font_colour)
    display.blit(text, (scale, scale))

def show_level():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Level: " + str(level), True, font_colour)
    display.blit(text, (90 - scale, scale))

def gameLoop():
    global score, level, SPEED

    snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    food = Food()
    food.new_location(snake.history)
    last_food_time = pygame.time.get_ticks()

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
        
        # Update food timer and respawn if needed
        if not food.update_timer():
            food.new_location(snake.history)
            last_food_time = pygame.time.get_ticks()
        
        food.show()
        show_score()
        show_level()

        if snake.check_eaten(food):
            score += food.weight
            food.new_location(snake.history)
            snake.grow()

        if snake.check_level():
            level += 1
            SPEED += 1
            snake.grow()

        if snake.death() or snake.history[0][0] < 0 or snake.history[0][0] >= SCREEN_WIDTH or snake.history[0][1] < 0 or snake.history[0][1] >= SCREEN_HEIGHT:
            score = 0
            level = 0
            SPEED = 9
            font = pygame.font.SysFont(None, 80)
            text = font.render("ЖЫЛАН ПОГИБ", True, defeat_colour)
            display.blit(text, (50, 200))
            pygame.display.update()
            time.sleep(3)
            snake.reset()
            food.new_location(snake.history)

        pygame.display.update()
        clock.tick(SPEED)

gameLoop()