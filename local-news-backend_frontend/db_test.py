import psycopg2

try:
    conn = psycopg2.connect(
        dbname="local_news",
        user="postgres",
        password="7080",
        host="localhost",
        port="5432"
    )
    print("✅ Database connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Error:", e)
