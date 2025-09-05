import psycopg

# PostgreSQL məlumatları
conn = psycopg.connect(
    host="localhost",     
    dbname="CubeSat",
    user="postgres",
    password="admin"  
)

cur = conn.cursor()

# Test üçün cədvəl yaratmaq
cur.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name TEXT);")
conn.commit()

# Məlumat əlavə etmək
cur.execute("INSERT INTO test_table (name) VALUES (%s)", ("Zehra",))
conn.commit()

# Məlumat oxumaq
cur.execute("SELECT * FROM test_table;")
rows = cur.fetchall()
print(rows)

cur.close()
conn.close()
