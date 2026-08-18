import os
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chicago_crime.db")


def get_conn():
    return sqlite3.connect(DB_PATH)




def load_summary():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM chicago_crime", conn)
    conn.close()
    return {
        "rows": len(df),
        "cols": df.shape[1],
        "unique_crime_types": int(df["primary_type"].nunique()),
        "arrest_rate": round(df["arrest"].mean() * 100, 2),
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
    }



def uc1_schema_info():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM chicago_crime", conn)
    conn.close()

    dtypes = df.dtypes.astype(str).reset_index()
    dtypes.columns = ["Column", "Type"]

    missing_pct = (df.isna().mean() * 100).round(2).sort_values(ascending=False)
    missing_pct = missing_pct[missing_pct > 0].reset_index()
    missing_pct.columns = ["Column", "Missing %"]

    return {
        "shape": df.shape,
        "dtypes_table": dtypes.to_html(classes="table table-sm table-striped", index=False),
        "missing_table": missing_pct.to_html(classes="table table-sm table-striped", index=False),
        "unique_crime_types": int(df["primary_type"].nunique()),
        "head_table": df.head(10).to_html(classes="table table-sm table-bordered", index=False),
    }



def crime_by_year():
    conn = get_conn()
    df = pd.read_sql(
        "SELECT year, COUNT(*) AS crime_count FROM chicago_crime GROUP BY year ORDER BY year",
        conn,
    )
    conn.close()
    return df


def top10_crime_categories():
    conn = get_conn()
    df = pd.read_sql(
        """SELECT primary_type, COUNT(*) AS cnt,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM chicago_crime), 2) AS pct
           FROM chicago_crime GROUP BY primary_type ORDER BY cnt DESC LIMIT 10""",
        conn,
    )
    conn.close()
    return df


def arrest_rate_overall():
    conn = get_conn()
    df = pd.read_sql("SELECT arrest FROM chicago_crime", conn)
    conn.close()
    return round(df["arrest"].mean() * 100, 2)


def top10_community_areas():
    conn = get_conn()
    df = pd.read_sql(
        """SELECT community_code, COUNT(*) AS crime_count
           FROM chicago_crime GROUP BY community_code
           ORDER BY crime_count DESC LIMIT 10""",
        conn,
    )
    conn.close()
    return df



def crime_outlier_areas():
    conn = get_conn()
    df = pd.read_sql(
        "SELECT community_code, COUNT(*) AS cnt FROM chicago_crime GROUP BY community_code",
        conn,
    )
    conn.close()
    values = df["cnt"].values
    q1, q3 = np.percentile(values, 25), np.percentile(values, 75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = df[(df["cnt"] < lower) | (df["cnt"] > upper)]
    return {
        "q1": q1, "q3": q3, "iqr": iqr,
        "lower": round(lower, 2), "upper": round(upper, 2),
        "outliers_table": outliers.to_html(classes="table table-sm table-striped", index=False),
    }


def correlation_table():
    conn = get_conn()
    df = pd.read_sql("SELECT year, arrest, domestic FROM chicago_crime", conn)
    conn.close()
    df["arrest"] = df["arrest"].astype(int)
    df["domestic"] = df["domestic"].astype(int)
    corr = df.corr().round(3)
    return corr.to_html(classes="table table-sm table-bordered")



def yearly_view():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM vw_crime_yearly", conn)
    conn.close()
    return df


def category_view():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM vw_crime_by_category ORDER BY total DESC", conn)
    conn.close()
    return df


def top5_crime_types_pct():
    conn = get_conn()
    df = pd.read_sql(
        """SELECT primary_type, COUNT(*) AS cnt,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM chicago_crime), 2) AS pct
           FROM chicago_crime GROUP BY primary_type ORDER BY cnt DESC LIMIT 5""",
        conn,
    )
    conn.close()
    return df


def arrests_per_year():
    conn = get_conn()
    df = pd.read_sql(
        "SELECT year, SUM(arrest) AS arrests FROM chicago_crime GROUP BY year ORDER BY year",
        conn,
    )
    conn.close()
    return df