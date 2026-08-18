import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chicago_crime.db")
OUTPUTS_DIR = os.path.join(BASE_DIR, "..", "outputs")

os.makedirs(OUTPUTS_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM chicago_crime", conn)
conn.close()

df['date'] = pd.to_datetime(df['date'])

#1: Crime Trend Over Years
print("1: CRIME TREND OVER YEARS")
yearly = df.groupby('year').size()
plt.figure(figsize=(10, 6))
yearly.plot(kind='line', marker='o', color='steelblue')
plt.title("Total Crimes Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Crimes")
plt.grid(True)
plt.savefig(os.path.join(OUTPUTS_DIR, "07_crime_trend_yearly.png"))
plt.close()
print(yearly)

#2: Crime Distribution by Category
print("\n2: CRIME DISTRIBUTION BY CATEGORY")
top10_types = df['primary_type'].value_counts().head(10)
top10_pct = (top10_types / len(df) * 100).round(2)
plt.figure(figsize=(10, 6))
top10_types.plot(kind='bar', color='steelblue')
plt.title("Top 10 Crime Categories")
plt.xlabel("Primary Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "08_top10_crime_categories.png"))
plt.close()
print("Counts:\n", top10_types)
print("\nPercentages:\n", top10_pct)

#3: Arrests and Crime Outcomes
print("\n3: ARRESTS AND CRIME OUTCOMES")
arrest_rate = df['arrest'].mean() * 100
print(f"Overall arrest rate: {arrest_rate:.2f}%")

#4: Heatmap of Crime by Month and Day of Week
print("\n4: HEATMAP - MONTH VS DAY OF WEEK")
pivot = df.pivot_table(index='crime_month', columns='crime_dayofweek', values='id', aggfunc='count')
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = pivot[day_order]
plt.figure(figsize=(10, 8))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title("Crime Frequency: Month vs Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Month")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "09_heatmap_month_dayofweek.png"))
plt.close()
print("Heatmap saved.")

#5: Top Community Areas
print("\n5: TOP COMMUNITY AREAS")
top_areas = df['community_code'].value_counts().head(10)
plt.figure(figsize=(10, 6))
top_areas.plot(kind='bar', color='darkgreen')
plt.title("Top 10 Community Areas by Crime Count")
plt.xlabel("Community Code")
plt.ylabel("Crime Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "10_top10_community_areas.png"))
plt.close()
print(top_areas)

#Use Case 2 Questions
print("\nUSE CASE 2 — FINAL ANSWERS")
print("Most frequent crime category:", df['primary_type'].value_counts().idxmax())

arrest_by_year = (df.groupby('year')['arrest'].mean() * 100).round(2)
print("\nArrest rate by year (consistency check):\n", arrest_by_year)

month_freq = df.groupby('crime_month').size()
print("\nMonth with highest crime frequency:", month_freq.idxmax(), "with", month_freq.max(), "crimes")
