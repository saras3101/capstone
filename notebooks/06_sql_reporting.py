import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chicago_crime.db")
OUTPUTS_DIR = os.path.join(BASE_DIR, "..", "outputs")

os.makedirs(OUTPUTS_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

#2: SQL Queries
print("2: SQL QUERIES")

print("\n Crime count per year ")
q1 = "SELECT year, COUNT(*) AS crime_count FROM chicago_crime GROUP BY year ORDER BY year;"
df_q1 = pd.read_sql(q1, conn)
print(df_q1)

print("\n Top 5 crime types and their percentages ")
q2 = """
SELECT primary_type, 
       COUNT(*) AS cnt, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM chicago_crime), 2) AS pct
FROM chicago_crime 
GROUP BY primary_type 
ORDER BY cnt DESC 
LIMIT 5;
"""
df_q2 = pd.read_sql(q2, conn)
print(df_q2)

print("\n Arrest count per year ")
q3 = "SELECT year, SUM(arrest) AS arrests FROM chicago_crime GROUP BY year ORDER BY year;"
df_q3 = pd.read_sql(q3, conn)
print(df_q3)

# 3: Database Stored Views 
print("\n 3: CREATE VIEWS ")

cursor.execute("DROP VIEW IF EXISTS vw_crime_yearly;")
cursor.execute("""
CREATE VIEW vw_crime_yearly AS 
SELECT year, COUNT(*) AS total 
FROM chicago_crime 
GROUP BY year;
""")

cursor.execute("DROP VIEW IF EXISTS vw_crime_by_category;")
cursor.execute("""
CREATE VIEW vw_crime_by_category AS 
SELECT primary_type, COUNT(*) AS total 
FROM chicago_crime 
GROUP BY primary_type;
""")

conn.commit()
print("Views created: vw_crime_yearly, vw_crime_by_category")

#4: Pandas Integration 
print("\n=== TASK 4: READ VIEWS INTO PANDAS ===")

yearly_view_df = pd.read_sql("SELECT * FROM vw_crime_yearly", conn)
print("\nvw_crime_yearly:\n", yearly_view_df)

category_view_df = pd.read_sql("SELECT * FROM vw_crime_by_category", conn)
print("\nvw_crime_by_category:\n", category_view_df)

#5: Visualization from SQL Data
print("\n=== TASK 5: VISUALIZATION FROM SQL DATA ===")

plt.figure(figsize=(10, 6))
plt.bar(yearly_view_df['year'].astype(str), yearly_view_df['total'], color='teal')
plt.title("Crime Count Per Year (from vw_crime_yearly)")
plt.xlabel("Year")
plt.ylabel("Total Crimes")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "05_sql_crime_per_year.png"))
plt.close()

plt.figure(figsize=(10, 6))
top_categories = category_view_df.sort_values('total', ascending=False).head(10)
sns.barplot(data=top_categories, x='total', y='primary_type', palette='viridis')
plt.title("Crime Categories (from vw_crime_by_category)")
plt.xlabel("Total Crimes")
plt.ylabel("Primary Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "06_sql_crime_by_category.png"))
plt.close()

print("Charts saved to", os.path.join(OUTPUTS_DIR, "05_sql_crime_per_year.png"),
      "and", os.path.join(OUTPUTS_DIR, "06_sql_crime_by_category.png"))

conn.close()
