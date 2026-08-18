# Chicago Crime Analytics — Web Application

A Flask-based reporting dashboard built on top of the Chicago Police Department (CPD) crime data pipeline. This web app serves as the presentation layer for the four use cases delivered as part of the Python Full Stack capstone project.

## Project Overview

CPD crime data (2015–2023) is ingested, cleaned, stored, and analyzed through a Python pipeline (Pandas, NumPy, SQLite). This web app exposes those results through a browser-based dashboard, satisfying the "web application" and "exports reports" requirements of the capstone brief.

**Pipeline:** `Ingest → Clean → Store → Analyze → Report`

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Data storage | SQLite (`chicago_crime.db`) |
| Data processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn (pre-generated charts) |
| Frontend | Jinja2 templates + Bootstrap 5 |
| Report export | FPDF2 (PDF generation) |

## Features by Use Case

| Route | Description |
|---|---|
| `/` | Overview dashboard — total records, columns, unique crime types, overall arrest rate, date range, and a PDF export button |
| `/usecase1` | Data schema, dtypes, missing-value breakdown, and first 10 rows of the cleaned dataset |
| `/usecase2` | Crime trend by year, top 10 crime categories, arrest rate, month-vs-day heatmap, top community areas |
| `/usecase3` | Crime intensity by hour, community area outlier detection (IQR method), correlation matrix |
| `/usecase4` | Top 5 crime types, arrest count per year, live-queried SQL views (`vw_crime_yearly`, `vw_crime_by_category`) |
| `/export/summary-report` | Generates and downloads a PDF summary report on demand |

All tables and charts are queried live from `chicago_crime.db` at request time — nothing is hardcoded.

## Project Structure

```
webapp/
├── app.py              # Flask routes
├── analysis.py         # SQL queries / Pandas logic, returns data (not print statements)
├── templates/
│   ├── base.html        # Shared layout + nav bar
│   ├── home.html
│   ├── uc1.html
│   ├── uc2.html
│   ├── uc3.html
│   └── uc4.html
└── static/
    └── charts/          # Pre-generated PNG charts from the analysis pipeline
```

## How to Run

1. Ensure `chicago_crime.db` exists at `../data/chicago_crime.db` (relative to `webapp/`) — created by running the Use Case 1–4 pipeline scripts first.
2. Install dependencies:
   ```
   pip install flask pandas numpy fpdf2
   ```
3. From the `webapp/` directory:
   ```
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in a browser.

## Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/87cc00e7-2b50-4137-b417-d23f11be3e16" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/65162393-a615-4bf0-b0dc-e866711f8982" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/caffaad4-8928-49b0-8f7e-46f6de82e679" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/19de7759-f0fb-42a9-830e-ba2494a8f849" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/43dbb8ca-61a7-4fe4-bc02-01ef29bfa555" />


## Notes for Evaluators

- The web app is **read-only / reporting-focused** by design — CPD's requirement was analysis and reporting, not manual data entry (no CRUD operations).
- Database inserts, cleaning, and view creation happen in the pipeline scripts (Use Cases 1 and 4); this app only reads and presents that data.
- Charts are saved as static images from the original Matplotlib/Seaborn scripts to preserve exact output; tables are rendered live via SQL queries on each page load.
