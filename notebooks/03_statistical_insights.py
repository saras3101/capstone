import pandas as pd
import numpy as np
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

#1: Crime Intensity by Time
print("1: CRIME INTENSITY BY TIME")
df['Hour'] = df['date'].dt.hour
crimes_by_hour = df.groupby('Hour').size()
plt.figure(figsize=(10, 6))
crimes_by_hour.plot(kind='line', marker='o', color='crimson')
plt.title("Crimes by Hour of Day")
plt.xlabel("Hour (0-23)")
plt.ylabel("Number of Crimes")
plt.grid(True)
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "11_crimes_by_hour.png"))
plt.close()
print(crimes_by_hour)

#2: Community Area Clusters Using NumPy
print("\n2: COMMUNITY AREA CLUSTERS (NUMPY)")
mean_per_area = df.groupby('community_code').size()
plt.figure(figsize=(8, 6))
plt.boxplot(mean_per_area.values)
plt.title("Crime Count Distribution Across Community Areas")
plt.ylabel("Crime Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "12_community_area_boxplot.png"))
plt.close()

Q1 = np.percentile(mean_per_area, 25)
Q3 = np.percentile(mean_per_area, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = mean_per_area[(mean_per_area < lower_bound) | (mean_per_area > upper_bound)]
print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
print(f"Outlier bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
print("\nOutlier community areas (extreme crime counts):\n", outliers)

#3: Crime Cross-Correlation
print("\n3: CRIME CROSS-CORRELATION")
numeric_df = df[['year', 'crime_month', 'arrest', 'domestic']].copy()
numeric_df['arrest'] = numeric_df['arrest'].astype(int)
numeric_df['domestic'] = numeric_df['domestic'].astype(int)
corr = numeric_df.corr()
print(corr)
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title("Correlation Matrix: Year, Month, Arrest, Domestic")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUTS_DIR, "13_correlation_matrix.png"))
plt.close()
print("\nCorrelation heatmap saved.")
