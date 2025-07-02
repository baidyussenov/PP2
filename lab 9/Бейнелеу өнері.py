import pygame

pygame.init()
screen = pygame.display.set_mode((900, 650))
pygame.display.set_caption("БЕЙНЕЛЕУ ӨНЕРІ 2.0")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GRAY  = (200, 200, 200)

# Панель
TOOLBAR_HEIGHT = 100
screen.fill(WHITE)

# Переменные состояния
current_color = BLACK
tool = 'brush'
drawing = False
start_pos = None
last_pos = None
radius = 5

# Кнопки инструментов
buttons = {
    'brush': pygame.Rect(10, 10, 80, 40),
    'rect': pygame.Rect(100, 10, 80, 40),
    'circle': pygame.Rect(190, 10, 80, 40),
    'square': pygame.Rect(280, 10, 80, 40),
    'right_triangle': pygame.Rect(370, 10, 110, 40),
    'equilateral_triangle': pygame.Rect(490, 10, 130, 40),
    'rhombus': pygame.Rect(630, 10, 80, 40),
    'eraser': pygame.Rect(720, 10, 80, 40),
    'red': pygame.Rect(820, 10, 30, 30),
    'green': pygame.Rect(820, 45, 30, 30),
    'blue': pygame.Rect(860, 10, 30, 30),
    'black': pygame.Rect(860, 45, 30, 30)
}

# Панель инструментов
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, 900, TOOLBAR_HEIGHT))
    font = pygame.font.SysFont(None, 20)
    for name, rect in buttons.items():
        if name in ['red', 'green', 'blue', 'black']:
            pygame.draw.rect(screen, eval(name.upper()), rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            label = font.render(name.replace('_', ' '), True, BLACK)
            screen.blit(label, (rect.x + 4, rect.y + 10))

# Получение цвета по кнопке
def get_color_from_button(name):
    if name == 'red': return RED
    if name == 'green': return GREEN
    if name == 'blue': return BLUE
    if name == 'black': return WHITE  # ластик
    return BLACK

# Прямоугольник
def draw_rectangle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, width)

# Круг
def draw_circle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2)//2, (y1 + y2)//2)
    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
    pygame.draw.circle(surface, color, center, radius, width)

# Квадрат
def draw_square(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, width)

# Прямоугольный треугольник
def draw_right_triangle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    points = [start, (x1, y2), end]
    pygame.draw.polygon(surface, color, points, width)

# Равносторонний треугольник
def draw_equilateral_triangle(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    base = abs(x2 - x1)
    height = int(base * (3**0.5) / 2)
    cx = (x1 + x2) // 2
    top = (cx, y1 - height)
    points = [top, (x1, y1), (x2, y1)]
    pygame.draw.polygon(surface, color, points, width)

# Ромб
def draw_rhombus(surface, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    dx = abs(x2 - x1) // 2
    dy = abs(y2 - y1) // 2
    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, points, width)

# Основной цикл
def main():
    global tool, current_color, drawing, start_pos, last_pos

    canvas = screen.copy()  # для постоянного рисования

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < TOOLBAR_HEIGHT:
                    for name, rect in buttons.items():
                        if rect.collidepoint(mx, my):
                            if name in ['brush', 'rect', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus', 'eraser']:
                                tool = name
                            else:
                                current_color = get_color_from_button(name)
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    if tool == 'rect':
                        draw_rectangle(canvas, start_pos, end_pos, current_color)
                    elif tool == 'circle':
                        draw_circle(canvas, start_pos, end_pos, current_color)
                    elif tool == 'square':
                        draw_square(canvas, start_pos, end_pos, current_color)
                    elif tool == 'right_triangle':
                        draw_right_triangle(canvas, start_pos, end_pos, current_color)
                    elif tool == 'equilateral_triangle':
                        draw_equilateral_triangle(canvas, start_pos, end_pos, current_color)
                    elif tool == 'rhombus':
                        draw_rhombus(canvas, start_pos, end_pos, current_color)
                drawing = False
                last_pos = None

            elif event.type == pygame.MOUSEMOTION and drawing:
                if tool in ['brush', 'eraser'] and last_pos:
                    color = WHITE if tool == 'eraser' else current_color
                    pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                    last_pos = event.pos

        # Обновление экрана
        screen.blit(canvas, (0, 0))

        # Временная фигура (предпросмотр)
        if drawing and tool in ['rect', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
            preview = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            preview_color = (*current_color, 120)
            mouse_pos = pygame.mouse.get_pos()
            if tool == 'rect':
                draw_rectangle(preview, start_pos, mouse_pos, preview_color)
            elif tool == 'circle':
                draw_circle(preview, start_pos, mouse_pos, preview_color)
            elif tool == 'square':
                draw_square(preview, start_pos, mouse_pos, preview_color)
            elif tool == 'right_triangle':
                draw_right_triangle(preview, start_pos, mouse_pos, preview_color)
            elif tool == 'equilateral_triangle':
                draw_equilateral_triangle(preview, start_pos, mouse_pos, preview_color)
            elif tool == 'rhombus':
                draw_rhombus(preview, start_pos, mouse_pos, preview_color)
            screen.blit(preview, (0, 0))

        draw_toolbar()
        pygame.display.flip()

    pygame.quit()

main()
