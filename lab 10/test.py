import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Post9992k",
        options='-c client_encoding=UTF8'
    )
    print("✅ Успешное подключение к PostgreSQL")
    conn.close()
except Exception as e:
    print("❌ Ошибка подключения:", e)
