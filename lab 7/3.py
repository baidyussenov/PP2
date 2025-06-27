import pygame, os

# --- Инициализация Pygame и создание окна ---
pygame.init()
screen = pygame.display.set_mode((800, 500))  # окно 800x500
pygame.display.set_caption("Музыкальный плеер")
clock = pygame.time.Clock()  # для ограничения FPS

# --- Загрузка музыкальных файлов ---
music_folder = "lab 7/musics"
# создаём список всех mp3-файлов из папки
playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]

# --- Загрузка и растягивание фонового изображения ---
bg = pygame.image.load("lab 7/background1.png")
bg = pygame.transform.scale(bg, (800, 500))  # подгоняем под размер окна

# --- Подготовка шрифта для отображения названия трека ---
font = pygame.font.SysFont(None, 20)

# --- Утилита для загрузки и масштабирования изображений кнопок ---
def load(name, size):
    return pygame.transform.scale(pygame.image.load(f"lab 7/{name}.png"), size)

# --- Загрузка изображений кнопок управления ---
play_img  = load("play", (60, 60))    # кнопка воспроизведения
pause_img = load("pause", (60, 60))   # кнопка паузы
next_img  = load("next", (60, 60))    # кнопка следующего трека
prev_img  = load("back", (60, 60))    # кнопка предыдущего трека

# --- Позиции прямоугольников кнопок (для обработки кликов) ---
panel_y = 420  # координата Y панели с кнопками
play_r  = pygame.Rect(370, panel_y + 20, 60, 60)
next_r  = pygame.Rect(440, panel_y + 20, 60, 60)
prev_r  = pygame.Rect(300, panel_y + 20, 60, 60)

# --- Переменные состояния ---
index = 0            # индекс текущей песни
volume = 0.5         # громкость от 0.0 до 1.0
playing = True       # играет ли музыка

# --- Начальное воспроизведение первой песни ---
pygame.mixer.music.load(playlist[index])
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play()

# --- Основной цикл приложения ---
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False  # выход из программы

        # --- Управление с клавиатуры ---
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:  # пауза/продолжить
                pygame.mixer.music.pause() if playing else pygame.mixer.music.unpause()
                playing = not playing  # переключаем состояние
            elif e.key == pygame.K_RIGHT:  # следующая песня
                index = (index + 1) % len(playlist)
            elif e.key == pygame.K_LEFT:   # предыдущая песня
                index = (index - 1) % len(playlist)
            elif e.key == pygame.K_UP:     # увеличить громкость
                volume = min(1.0, volume + 0.1)
            elif e.key == pygame.K_DOWN:   # уменьшить громкость
                volume = max(0.0, volume - 0.1)

            # применить громкость
            pygame.mixer.music.set_volume(volume)

            # если трек был переключён, запускаем его
            if e.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                pygame.mixer.music.load(playlist[index])
                pygame.mixer.music.play()
                playing = True

        # --- Управление с мыши (клики по кнопкам) ---
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if play_r.collidepoint(e.pos):  # нажата кнопка play/pause
                pygame.mixer.music.pause() if playing else pygame.mixer.music.unpause()
                playing = not playing
            elif next_r.collidepoint(e.pos):  # следующая песня
                index = (index + 1) % len(playlist)
                pygame.mixer.music.load(playlist[index])
                pygame.mixer.music.play()
                playing = True
            elif prev_r.collidepoint(e.pos):  # предыдущая песня
                index = (index - 1) % len(playlist)
                pygame.mixer.music.load(playlist[index])
                pygame.mixer.music.play()
                playing = True

    # --- Отрисовка интерфейса ---
    screen.blit(bg, (0, 0))  # фон на весь экран

    # белая панель снизу (просто прямоугольник)
    pygame.draw.rect(screen, (255, 255, 255), (155, panel_y, 500, 100))

    # название текущего трека
    track_name = os.path.basename(playlist[index])
    text = font.render(track_name, True, (20, 20, 50))
    screen.blit(text, (360, panel_y + 5))

    # отрисовка кнопок
    screen.blit(pause_img if playing else play_img, (play_r.x, play_r.y))
    screen.blit(next_img, (next_r.x, next_r.y))
    screen.blit(prev_img, (prev_r.x, prev_r.y))

    # обновляем экран
    pygame.display.update()
    clock.tick(24)

# --- Завершение Pygame ---
pygame.quit()
