import psycopg2
import pygame
import random
import csv
import sys
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Post9992k",
    options='-c client_encoding=UTF8'
)

cur = conn.cursor()

# Создание таблиц, если их нет
cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    score INTEGER,
    level INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
""")
conn.commit()

# Работа с телефонной книгой
def insert_from_csv(path):
    with open(path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) != 2: continue
            name, phone = row
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", (name, phone))
    conn.commit()
    print("✅ CSV импортирован.")

def insert_from_console():
    name = input("Имя: ")
    phone = input("Телефон: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", (name, phone))
    conn.commit()
    print("✅ Добавлено.")

def update_user(old, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET first_name=%s WHERE first_name=%s OR phone=%s", (new_name, old, old))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s OR phone=%s", (new_phone, old, old))
    conn.commit()
    print("✅ Обновлено.")

def query_users(filter_text=None):
    if filter_text:
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone ILIKE %s", (f"%{filter_text}%", f"%{filter_text}%"))
    else:
        cur.execute("SELECT * FROM phonebook")
    for row in cur.fetchall():
        print(row)

def delete_user(identifier):
    cur.execute("DELETE FROM phonebook WHERE first_name=%s OR phone=%s", (identifier, identifier))
    conn.commit()
    print("🗑️ Удалено.")

# Работа с пользователями игры
def get_or_create_user(username):
    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
        print("🎮 Добро пожаловать обратно,", username)
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        print("🎮 Новый игрок:", username)

    cur.execute("SELECT score, level FROM user_score WHERE user_id=%s ORDER BY id DESC LIMIT 1", (user_id,))
    score_row = cur.fetchone()
    return user_id, score_row[0] if score_row else 0, score_row[1] if score_row else 1

def save_progress(user_id, username, score, level):
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    cur.execute("SELECT id, score FROM leaderboard WHERE username=%s", (username,))
    row = cur.fetchone()
    if row:
        if score > row[1]:
            cur.execute("UPDATE leaderboard SET score=%s, level=%s, created_at=NOW() WHERE id=%s", (score, level, row[0]))
            print("🏆 Рекорд обновлён!")
    else:
        cur.execute("INSERT INTO leaderboard (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
    conn.commit()
    print("💾 Прогресс сохранён.")

def show_leaderboard():
    cur.execute("SELECT username, score, level, created_at FROM leaderboard ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()
    print("\n🌟 ТОП-10 лучших игр:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]}: {row[1]} очков, Уровень {row[2]}, {row[3]}")

def close_connection():
    cur.close()
    conn.close()

# Игра Snake
def snake_game(user_id, username, last_level):
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    BLOCK = 20
    GRID_W, GRID_H = WIDTH // BLOCK, HEIGHT // BLOCK
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    def draw_text(txt, x, y):
        screen.blit(font.render(txt, True, (255,255,255)), (x, y))

    def gen_food(snake):
        while True:
            pos = (random.randint(0, GRID_W-1), random.randint(0, GRID_H-1))
            if pos not in snake:
                return {"pos": pos, "weight": random.randint(1,3), "timer": random.randint(30, 60),
                        "color": (random.randint(100,255), random.randint(100,255), random.randint(100,255))}

    snake = [(5,5), (4,5), (3,5)]
    direction = (1, 0)
    food = gen_food(snake)
    score = 0
    level = 1
    speed = 10
    hue = 0
    running = True

    while running:
        screen.fill((30,30,30))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, 1): direction = (0, -1)
                elif e.key == pygame.K_DOWN and direction != (0, -1): direction = (0, 1)
                elif e.key == pygame.K_LEFT and direction != (1, 0): direction = (-1, 0)
                elif e.key == pygame.K_RIGHT and direction != (-1, 0): direction = (1, 0)
                elif e.key == pygame.K_p:
                    save_progress(user_id, username, score, level)
                    print("⏸️ Прогресс сохранён (пауза).")

        new_head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
        if new_head in snake or not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            print("💀 Игра окончена!")
            save_progress(user_id, username, score, level)
            break

        snake.insert(0, new_head)

        if new_head == food["pos"]:
            score += food["weight"]
            if score % 5 == 0:
                level += 1
                speed += 1
            food = gen_food(snake)
        else:
            snake.pop()
            food["timer"] -= 1
            if food["timer"] <= 0:
                food = gen_food(snake)

        hue = (hue + 5) % 360
        for i, s in enumerate(snake):
            c = pygame.Color(0)
            c.hsva = ((hue + i*10) % 360, 100, 100, 100)
            pygame.draw.rect(screen, c, (s[0]*BLOCK, s[1]*BLOCK, BLOCK, BLOCK), border_radius=3)

        fx, fy = food["pos"]
        pygame.draw.circle(screen, food["color"], (fx*BLOCK+BLOCK//2, fy*BLOCK+BLOCK//2), BLOCK//2 - 2)

        draw_text(f"Очки: {score}", 10, 10)
        draw_text(f"Уровень: {level}", 10, 40)
        draw_text(f"Скорость: {speed}", 10, 70)
        draw_text("Нажмите 'P' чтобы сохранить", 10, HEIGHT-30)

        pygame.display.flip()
        clock.tick(speed)
    pygame.quit()

# Меню
if __name__ == "__main__":
    while True:
        print("\n📋 Главное меню:")
        print("1. Импорт из CSV")
        print("2. Добавить вручную")
        print("3. Обновить")
        print("4. Поиск")
        print("5. Удалить")
        print("6. Играть в Snake")
        print("7. Топ-10")
        print("8. Выйти")
        ch = input("Выбор: ")

        if ch == "1": insert_from_csv(input("Путь к CSV: "))
        elif ch == "2": insert_from_console()
        elif ch == "3":
            old = input("Имя или номер: ")
            newn = input("Новое имя (Enter чтобы пропустить): ")
            newp = input("Новый номер (Enter чтобы пропустить): ")
            update_user(old, newn if newn else None, newp if newp else None)
        elif ch == "4": query_users(input("Введите фильтр (или Enter): "))
        elif ch == "5": delete_user(input("Имя или номер для удаления: "))
        elif ch == "6":
            username = input("Введите имя игрока: ")
            uid, _, last_lvl = get_or_create_user(username)
            snake_game(uid, username, last_lvl)
        elif ch == "7": show_leaderboard()
        elif ch == "8": break
        else: print("⛔ Неверный выбор.")

    close_connection()
