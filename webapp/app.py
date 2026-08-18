from flask import Flask, render_template, send_file
import io
import analysis

app = Flask(__name__)


@app.route("/")
def home():
    summary = analysis.load_summary()
    return render_template("home.html", summary=summary)


@app.route("/usecase1")
def usecase1():
    info = analysis.uc1_schema_info()
    return render_template("uc1.html", info=info)


@app.route("/usecase2")
def usecase2():
    yearly = analysis.crime_by_year()
    top10 = analysis.top10_crime_categories()
    areas = analysis.top10_community_areas()
    arrest_rate = analysis.arrest_rate_overall()
    return render_template(
        "uc2.html",
        yearly_table=yearly.to_html(classes="table table-sm table-striped", index=False),
        top10_table=top10.to_html(classes="table table-sm table-striped", index=False),
        areas_table=areas.to_html(classes="table table-sm table-striped", index=False),
        arrest_rate=arrest_rate,
    )


@app.route("/usecase3")
def usecase3():
    outliers = analysis.crime_outlier_areas()
    corr_table = analysis.correlation_table()
    return render_template("uc3.html", outliers=outliers, corr_table=corr_table)


@app.route("/usecase4")
def usecase4():
    yearly = analysis.yearly_view()
    category = analysis.category_view()
    top5 = analysis.top5_crime_types_pct()
    arrests = analysis.arrests_per_year()
    return render_template(
        "uc4.html",
        yearly_table=yearly.to_html(classes="table table-sm table-striped", index=False),
        category_table=category.to_html(classes="table table-sm table-striped", index=False),
        top5_table=top5.to_html(classes="table table-sm table-striped", index=False),
        arrests_table=arrests.to_html(classes="table table-sm table-striped", index=False),
    )


@app.route("/export/summary-report")
def export_summary_report():
    from fpdf import FPDF

    summary = analysis.load_summary()
    yearly = analysis.crime_by_year()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Chicago Crime Analytics - Summary Report", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Total Records: {summary['rows']}", ln=True)
    pdf.cell(0, 8, f"Unique Crime Types: {summary['unique_crime_types']}", ln=True)
    pdf.cell(0, 8, f"Overall Arrest Rate: {summary['arrest_rate']}%", ln=True)
    pdf.ln(4)
    pdf.cell(0, 8, "Crimes Per Year:", ln=True)
    for _, row in yearly.iterrows():
        pdf.cell(0, 7, f"  {row['year']}: {row['crime_count']}", ln=True)

    buf = io.BytesIO(pdf.output(dest="S"))
    buf.seek(0)
    return send_file(
        buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="crime_summary_report.pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)