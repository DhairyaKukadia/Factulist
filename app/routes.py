from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from app.models.bias_detector import analyze_bias
from app.models.credibility_checker import check_credibility
from app.services.report_generator import generate_report
from tinydb import TinyDB
import os
from newspaper import Article
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Explicitly define templates + static
bp = Blueprint(
    "routes",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

# TinyDB setup
reports_db = TinyDB("data/reports.json")


def scrape_url(url):
    """Extract article text from a URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"[Error scraping {url}]: {e}")
        return None


@bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = None
        url = request.form.get("url")

        if url:
            input_text = scrape_url(url)
        elif request.form.get("text"):
            input_text = request.form.get("text")
        elif "file" in request.files:
            file = request.files["file"]
            if file and file.filename:
                save_path = os.path.join("app", "uploads", file.filename)
                file.save(save_path)
                try:
                    with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
                        input_text = f.read()
                except Exception as e:
                    print(f"[Error reading file {file.filename}]: {e}")

        if not input_text:
            flash("Could not extract text. Try again.")
            return redirect(url_for("routes.home"))

        bias_result = analyze_bias(input_text)
        credibility_result = check_credibility(input_text, source=url) if url else check_credibility(input_text)

        report = generate_report(input_text, bias_result, credibility_result)
        reports_db.insert(report)

        return render_template("report.html", report=report)

    return render_template("index.html")


@bp.route("/history")
def history():
    all_reports = reports_db.all()
    last_reports = all_reports[-10:] if len(all_reports) > 10 else all_reports
    return render_template("history.html", reports=last_reports)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "POST":
        text1, text2 = None, None
        url1, url2 = request.form.get("url1"), request.form.get("url2")

        if url1:
            text1 = scrape_url(url1)
        elif request.form.get("text1"):
            text1 = request.form.get("text1")

        if url2:
            text2 = scrape_url(url2)
        elif request.form.get("text2"):
            text2 = request.form.get("text2")

        if not text1 or not text2:
            flash("Please provide both articles (URL or text).")
            return redirect(url_for("routes.compare"))

        bias1 = analyze_bias(text1)
        cred1 = check_credibility(text1, source=url1) if url1 else check_credibility(text1)
        report1 = generate_report(text1, bias1, cred1)

        bias2 = analyze_bias(text2)
        cred2 = check_credibility(text2, source=url2) if url2 else check_credibility(text2)
        report2 = generate_report(text2, bias2, cred2)

        return render_template("compare.html", report1=report1, report2=report2)

    return render_template("compare.html")


@bp.route("/export/latest")
def export_latest():
    all_reports = reports_db.all()
    if not all_reports:
        flash("No reports available to export.")
        return redirect(url_for("routes.history"))

    report = all_reports[-1]

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "Factulist Analysis Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, f"Date: {report.get('date', '—')}")
    pdf.drawString(50, height - 120, f"Title: {report.get('title', 'Untitled')}")

    pdf.drawString(50, height - 160, f"Bias: {report.get('bias_label', 'Unknown')} "
                                     f"({report.get('bias_score', 0)*100:.1f}%)")

    cred = report.get("credibility_raw", {})
    pdf.drawString(50, height - 190, f"Credibility Score: {cred.get('score', 0)}")
    pdf.drawString(70, height - 210, f"- Domain Score: {cred.get('domain_score', 0)}")
    pdf.drawString(70, height - 230, f"- References Score: {cred.get('refs_score', 0)} "
                                     f"(Refs found: {cred.get('refs_found', 0)})")
    pdf.drawString(70, height - 250, f"- Language Score: {cred.get('lang_score', 0)} "
                                     f"(Emotional words: {cred.get('emotional_words', 0)})")

    notes = report.get("notes", [])
    y = height - 290
    pdf.drawString(50, y, "Notes:")
    y -= 20
    for note in notes:
        pdf.drawString(70, y, f"- {note}")
        y -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="factulist_report.pdf", mimetype="application/pdf")
