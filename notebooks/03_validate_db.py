import sqlite3
conn = sqlite3.connect("data/chicago_crime.db")
cursor = conn.cursor()

for table in ['chicago_crime', 'iucr', 'police_beat_info', 'district_ps_info', 'ward_office', 'city_community']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(table, "row count:", cursor.fetchone()[0])

cursor.execute("SELECT * FROM chicago_crime LIMIT 3")
print("\nSample row:", cursor.fetchall()[0])

conn.close()