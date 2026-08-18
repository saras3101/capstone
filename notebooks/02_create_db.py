import sqlite3

conn = sqlite3.connect("data/chicago_crime.db")
cursor = conn.cursor()

with open("sql/schema_sqlite.sql", "r") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables created:", tables)

conn.close()