import pandas as pd
import numpy as np
import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "Chicago_Datasets_Python")
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chicago_crime.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "..", "sql", "schema_sqlite.sql")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("Old database removed.")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
with open(SCHEMA_PATH, "r") as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
conn.commit()
print("Schema created fresh.")

#Load
df = pd.read_csv(os.path.join(BASE_DIR, "..", "data", "Chicago_Datasets_Python", "chicago_crime_dataset.csv"))
print("\n1: LOAD DATASET ===")
print("Shape (rows, columns):", df.shape)
print("\nSchema / Data types:\n", df.dtypes)
print("\nFirst 10 rows:\n", df.head(10))

#Clean
print("\n2: CLEAN DATASET")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['date_of_update'] = pd.to_datetime(df['date_of_update'], errors='coerce')
print("Date column converted. Missing dates after conversion:", df['date'].isna().sum())

print("\nMissing values (%) per column:\n", (df.isna().mean() * 100).round(2).sort_values(ascending=False))

df['location_desc'] = df['location_desc'].fillna('UNKNOWN')

for col in ['primary_type', 'description', 'location_desc', 'block']:
    df[col] = df[col].astype(str).str.strip().str.upper()
print("\nCategorical fields standardized (stripped + uppercased).")
print("Sample primary_type values:", df['primary_type'].unique()[:5])

#Feature engineering
print("\n3: FEATURE ENGINEERING")
df['crime_month'] = df['date'].dt.month
df['crime_dayofweek'] = df['date'].dt.day_name()
print(df[['date', 'crime_month', 'crime_dayofweek']].head())

#NumPy missing value check
print("\n4: NUMPY MISSING VALUE ANALYSIS")
missing_pct = np.round(df.isna().mean().values * 100, 2)
cols_over_50 = df.columns[missing_pct > 50].tolist()
print("Columns with >50% missing:", cols_over_50 if cols_over_50 else "None — no columns dropped")

#Convert datetime to string for SQLite
df['date'] = df['date'].astype(str)
df['date_of_update'] = df['date_of_update'].astype(str)

#Insert lookup tables
print("\n5: INSERT INTO DATABASE")
iucr_df = pd.read_csv(os.path.join(DATA_DIR, "iucr_codes.csv"))
iucr_df.columns = iucr_df.columns.str.lower()
iucr_df.to_sql("iucr", conn, if_exists="append", index=False)

beat_df = pd.read_csv(os.path.join(DATA_DIR, "chicago_police_beat_info.csv"))
beat_df.columns = beat_df.columns.str.lower()
beat_df.to_sql("police_beat_info", conn, if_exists="append", index=False)

district_df = pd.read_csv(os.path.join(DATA_DIR, "chicago_district_ps_info.csv"))
district_df.columns = district_df.columns.str.lower()
district_df.to_sql("district_ps_info", conn, if_exists="append", index=False)

ward_df = pd.read_csv(os.path.join(DATA_DIR, "chicago_ward_offices.csv"))
ward_df.columns = ward_df.columns.str.lower()
ward_df.to_sql("ward_office", conn, if_exists="append", index=False)

community_df = pd.read_csv(os.path.join(DATA_DIR, "chicago_city_community.csv"))
community_df.columns = community_df.columns.str.lower()
community_df.to_sql("city_community", conn, if_exists="append", index=False)
print("Lookup tables loaded.")

df.to_sql("chicago_crime", conn, if_exists="append", index=False)
print("Crime table loaded:", len(df), "rows")

conn.close()

#Answer Use Case 1 questions
print("\nUSE CASE 1 — FINAL ANSWERS")
print("Unique crime types:", df['primary_type'].nunique())
print("Date range:", df['date'].min(), "to", df['date'].max())
print("Anomaly: Background states dataset covers 2012-2016, but actual range is", 
      df['date'].min(), "to", df['date'].max(), "- significant mismatch.")
