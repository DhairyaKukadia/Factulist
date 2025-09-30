from flask import Blueprint, render_template, request, jsonify, Response, send_file
from tinydb import TinyDB
import os, io, pandas as pd
from werkzeug.utils import secure_filename
from fpdf import FPDF
from app.services.report_generator import generate_report

bp = Blueprint("main", __name__)
db = TinyDB("data/reports.json")
source_db = TinyDB("data/sources.json")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ITEMS_PER_PAGE = 10

@bp.route("/", methods=["GET"])
def home():
    return render_template("report.html")

@bp.route("/check", methods=["POST"])
def check_article():
    if request.is_json:
        data = request.get_json()
        report = generate_report(data)
        return jsonify(report)

    url = request.form.get("url")
    raw_text = request.form.get("raw_text")
    file = request.files.get("file")

    input_data = {}
    if url:
        input_data["url"] = url
    elif raw_text:
        input_data["text"] = raw_text
    elif file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        input_data["file_path"] = file_path
    else:
        input_data = {}

    report = generate_report(input_data)
    return jsonify(report)

@bp.route("/history", methods=["GET"])
def history():
    reports = db.all()
    return render_template("history.html", reports=reports)

@bp.route("/sources", methods=["GET"])
def sources():
    sources = source_db.all()
    for s in sources:
        counts = s.get("counts", {})
        s["total"] = (
            counts.get("✅ Verified", 0)
            + counts.get("🟡 Mostly True", 0)
            + counts.get("🟠 Misleading", 0)
            + counts.get("❌ False", 0)
        )
    sources_sorted = sorted(sources, key=lambda x: x["total"], reverse=True)

    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    paginated_sources = sources_sorted[start:end]

    total_pages = (len(sources_sorted) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    return render_template(
        "sources.html",
        sources=paginated_sources,
        page=page,
        total_pages=total_pages
    )

# ----------------- Export Routes -----------------

@bp.route("/export/reports/csv", methods=["GET"])
def export_reports_csv():
    reports = db.all()
    if not reports:
        return "No data to export", 400
    df = pd.DataFrame(reports)
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=reports.csv"}
    )

@bp.route("/export/sources/csv", methods=["GET"])
def export_sources_csv():
    sources = source_db.all()
    if not sources:
        return "No data to export", 400
    df = pd.DataFrame(sources)
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sources.csv"}
    )

@bp.route("/export/report/<int:report_id>/pdf", methods=["GET"])
def export_report_pdf(report_id):
    reports = db.all()
    if report_id >= len(reports):
        return "Report not found", 404
    report = reports[report_id]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Factulist Credibility Report", ln=True, align="C")

    for key, value in report.items():
        pdf.multi_cell(0, 10, f"{key}: {value}")

    # Fix: cast output to str before encoding
    pdf_bytes = str(pdf.output(dest="S")).encode("latin-1")
    pdf_output = io.BytesIO(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name=f"report_{report_id}.pdf")
