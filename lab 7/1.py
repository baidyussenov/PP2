# Импортируем нужные библиотеки:
import pygame       # для графики
import sys          # для выхода из программы
import datetime     # для получения текущего времени

# Инициализируем Pygame
pygame.init()

# Создаём окно размером 1400x950 пикселей
screen = pygame.display.set_mode((1400, 950))

# Объект для управления частотой кадров
clock = pygame.time.Clock()

# Загружаем изображения: фон (часы) и две стрелки (минутная и секундная)
background = pygame.image.load("clock.png")
right_arm = pygame.image.load("rightarm.png")  # минутная стрелка
left_arm = pygame.image.load("leftarm.png")    # секундная стрелка

# Центр часов — точка, вокруг которой крутятся стрелки
# Подбирается вручную, зависит от размера clock.png
center = (699, 990)

# Получаем размеры изображений стрелок
rw, rh = right_arm.get_size()
lw, lh = left_arm.get_size()

# Функция для поворота стрелки и отрисовки её на экране
def blit_rotate(image, pos, origin, angle):
    # Вычисляем положение изображения с учётом точки поворота
    image_rect = image.get_rect(topleft=(pos[0] - origin[0], pos[1] - origin[1]))
    
    # Поворачиваем изображение на заданный угол
    rotated_image = pygame.transform.rotate(image, angle)

    # Вычисляем новое положение изображения после поворота
    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    # Отображаем повернутое изображение на экране
    screen.blit(rotated_image, rotated_rect.topleft)

# Главный цикл программы (работает всё время)
while True:
    # Проверяем события, например, нажатие на крестик (закрыть окно)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Получаем текущее время
    now = datetime.datetime.now()

    # Считаем секунды и минуты с учётом долей секунды
    seconds = now.second + now.microsecond / 950000
    minutes = now.minute + seconds / 60

    # Угол поворота для секундной стрелки: 6° на каждую секунду (360 / 60)
    angle_sec = -seconds * 6  # Минус — потому что вращение против часовой стрелки в Pygame

    # Угол для минутной стрелки: тоже 6° на каждую минуту, добавлен сдвиг +670 (подгон под картинку)
    angle_min = -minutes * 6 + 670

    # Рисуем фон (картинку часов)
    screen.blit(background, (0, 0))

    # Рисуем минутную стрелку, поворачиваем её на нужный угол
    # Точка поворота — примерно 95% от высоты (нижняя часть стрелки)
    blit_rotate(right_arm, center, (rw / 2, rh * 0.95), angle_min)

    # Рисуем секундную стрелку
    blit_rotate(left_arm, center, (lw / 2, lh * 0.95), angle_sec)

    # Рисуем зелёную точку в центре — ось стрелок
    pygame.draw.circle(screen, (0, 255, 0), center, 5)

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем FPS — 60 кадров в секунду
    clock.tick(60)
