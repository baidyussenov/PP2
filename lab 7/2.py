# Подключаем библиотеку для работы с графикой и играми
import pygame

# Запускаем все нужные части pygame
pygame.init()

# Размер окна (ширина 800, высота 600)
window_size = (800, 600)
font_colour = (0, 0, 0)
scale = 40

# Создаём окно игры
screen = pygame.display.set_mode(window_size)

# Название окна
pygame.display.set_caption("Бауырсақ")

font = pygame.font.SysFont(None, 36)


background = pygame.image.load("lab 7/forest.png")
background = pygame.transform.scale(background, window_size)  # Resize to window
 
def show_score():
    text = font.render(f"БАУЫРСАҚ", True, font_colour)
    screen.blit(text, (scale, scale))
# Цвет круга — чёрный
ball_color = pygame.Color('yellow')

# Цвет фона — белый
bg_color = pygame.Color('white')

# Начальная позиция круга — в центре экрана
ball_pos = [400, 300]  # [по X, по Y]

# Радиус круга
ball_radius = 25

# Скорость движения круга (на сколько пикселей двигается)
speed = 20


# Главный цикл игры — работает постоянно
while True:
    # Проверяем события (например, нажали на крестик окна)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Закрыть pygame
            exit()         # Выйти из программы

    # Смотрим, какие клавиши нажаты
    keys = pygame.key.get_pressed()

    # Если нажата стрелка вверх — двигаем круг вверх (уменьшаем Y)
    # Не даём выйти за верхнюю границу
    if keys[pygame.K_UP]:
        ball_pos[1] = max(ball_pos[1] - speed, ball_radius)

    # Если нажата стрелка вниз — двигаем круг вниз (увеличиваем Y)
    # Не даём выйти за нижнюю границу
    if keys[pygame.K_DOWN]:
        ball_pos[1] = min(ball_pos[1] + speed, window_size[1] - ball_radius)

    # Если нажата стрелка влево — двигаем круг влево (уменьшаем X)
    # Не даём выйти за левую границу
    if keys[pygame.K_LEFT]:
        ball_pos[0] = max(ball_pos[0] - speed, ball_radius)

    # Если нажата стрелка вправо — двигаем круг вправо (увеличиваем X)
    # Не даём выйти за правую границу
    if keys[pygame.K_RIGHT]:
        ball_pos[0] = min(ball_pos[0] + speed, window_size[0] - ball_radius)

   

    
   
    screen.blit(background, (0, 0))

    # Рисуем круг на экране в текущей позиции
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
    show_score()
    # Обновляем окно — показываем изменения
    pygame.display.flip()

    # Ждём немного, чтобы программа шла с нормальной скоростью (35 кадров в секунду)
    pygame.time.Clock().tick(35)
