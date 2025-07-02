import pygame  # импортируем библиотеку для рисования
pygame.init()  # инициализируем pygame

# создаём окно
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Бейнелеу өнері")
clock = pygame.time.Clock()  # чтобы управлять скоростью обновлений

# стандартные цвета (RGB — красный, зелёный, синий)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GRAY  = (200, 200, 200)

# высота панели инструментов сверху
TOOLBAR_HEIGHT = 60

# заливаем фон белым
screen.fill(WHITE)

# переменные для состояния программы
current_color = BLACK    # текущий цвет
tool = 'brush'           # текущий инструмент (кисть по умолчанию)
drawing = False          # рисуем ли сейчас?
start_pos = None         # где начали рисовать (позиция мыши)
last_pos = None          # последняя позиция мыши для непрерывной линии
radius = 5               # радиус кисти

# кнопки панели: название → прямоугольник (x, y, ширина, высота)
buttons = {
    'brush':     pygame.Rect(10, 10, 80, 40),
    'rect':      pygame.Rect(100, 10, 80, 40),
    'circle':    pygame.Rect(190, 10, 80, 40),
    'eraser':    pygame.Rect(280, 10, 80, 40),
    'red':       pygame.Rect(400, 10, 40, 40),
    'green':     pygame.Rect(450, 10, 40, 40),
    'blue':      pygame.Rect(500, 10, 40, 40),
    'black':     pygame.Rect(550, 10, 40, 40)
}

# рисуем панель инструментов (верхнюю часть экрана)
def draw_toolbar():
    # рисуем серую панель сверху
    pygame.draw.rect(screen, GRAY, (0, 0, 800, TOOLBAR_HEIGHT))
    font = pygame.font.SysFont(None, 24)  # шрифт для подписей

    for name, rect in buttons.items():
        # если кнопка — инструмент, то делаем серой
        color = GRAY if name in ['brush', 'rect', 'circle', 'eraser'] else eval(name.upper())

        pygame.draw.rect(screen, color, rect)        # заливка кнопки
        pygame.draw.rect(screen, BLACK, rect, 2)     # чёрная рамка

        if name in ['brush', 'rect', 'circle', 'eraser']:
            text = font.render(name, True, BLACK)    # подпись
            screen.blit(text, (rect.x + 5, rect.y + 10))

# возвращаем цвет по названию кнопки
def get_color_from_button(name):
    if name == 'red': return RED
    if name == 'green': return GREEN
    if name == 'blue': return BLUE
    if name == 'black': return WHITE  # "чёрная" кнопка — на самом деле это ластик (белый цвет)
    return BLACK

# рисуем прямоугольник по двум точкам (начало и конец)
def draw_rectangle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, width)

# рисуем круг между двумя точками
def draw_circle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2)//2, (y1 + y2)//2)
    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
    pygame.draw.circle(surface, color, center, radius, width)

# основная функция
def main():
    global tool, current_color, drawing, start_pos, last_pos

    # создаём "канвас" — это копия экрана, куда сохраняются все готовые рисунки
    canvas = screen.copy()

    running = True
    while running:
        clock.tick(60)  # 60 кадров в секунду

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # если нажата кнопка мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < TOOLBAR_HEIGHT:
                    # нажата кнопка на панели
                    for name, rect in buttons.items():
                        if rect.collidepoint(mx, my):
                            if name in ['brush', 'rect', 'circle', 'eraser']:
                                tool = name
                            else:
                                current_color = get_color_from_button(name)
                else:
                    # начало рисования на холсте
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            # отпустили мышь — заканчиваем рисование фигуры
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    if tool == 'rect':
                        draw_rectangle(canvas, start_pos, end_pos, current_color)
                    elif tool == 'circle':
                        draw_circle(canvas, start_pos, end_pos, current_color)
                drawing = False
                last_pos = None

            # движение мыши во время рисования
            elif event.type == pygame.MOUSEMOTION and drawing:
                if tool in ['brush', 'eraser'] and last_pos:
                    # рисуем линию от последней точки до текущей (чтобы не было разрывов)
                    color = WHITE if tool == 'eraser' else current_color
                    pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                    last_pos = event.pos

        # сначала рисуем "готовое" изображение
        screen.blit(canvas, (0, 0))

        # если рисуем прямоугольник или круг — отображаем временную прозрачную фигуру
        if drawing and tool in ['rect', 'circle']:
            preview_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            preview_color = (*current_color, 120)  # прозрачность 120 из 255

            if tool == 'rect':
                draw_rectangle(preview_surface, start_pos, pygame.mouse.get_pos(), preview_color)
            elif tool == 'circle':
                draw_circle(preview_surface, start_pos, pygame.mouse.get_pos(), preview_color)

            # накладываем прозрачную фигуру поверх канваса
            screen.blit(preview_surface, (0, 0))

        # рисуем панель
        draw_toolbar()

        pygame.display.flip()  # обновляем экран

    pygame.quit()  # закрываем приложение

main()
