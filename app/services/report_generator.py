import requests, pdfplumber, docx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tinydb import TinyDB, Query
from app.models.credibility_checker import classify_article
from app.models.bias_detector import detect_bias

db = TinyDB("data/reports.json")
source_db = TinyDB("data/sources.json")

def fetch_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "header", "footer", "nav"]):
            tag.extract()
        return " ".join(soup.stripped_strings)[:3000]
    except Exception as e:
        return f"Error fetching article: {e}"

def extract_pdf_text(file_path: str) -> str:
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + " "
        return text[:3000] if text.strip() else "Error: Could not extract text from PDF."
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_docx_text(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
        return text[:3000] if text.strip() else "Error: Could not extract text from DOCX."
    except Exception as e:
        return f"Error reading DOCX: {e}"

def update_source_stats(url: str, credibility: str):
    if url and url != "N/A":
        domain = urlparse(url).netloc.replace("www.", "")
        Source = Query()
        existing = source_db.get(Source.domain == domain)
        if existing and isinstance(existing, dict):
            counts = existing.get("counts", {})
            counts[credibility] = counts.get(credibility, 0) + 1
            source_db.update({"counts": counts}, Source.domain == domain)
        else:
            source_db.insert({"domain": domain, "counts": {credibility: 1}})

def build_corroborating_sources(text: str):
    """Generate keyword-based search links on trusted sites."""
    if not text or text.startswith("Error"):
        return ["https://www.reuters.com", "https://apnews.com"]

    # Take first 5 words as search query
    query_words = text.split()[:5]
    query = "+".join(query_words)

    return [
        f"https://www.reuters.com/site-search/?query={query}",
        f"https://apnews.com/search?q={query}"
    ]

def generate_report(input_data: dict) -> dict:
    text, url, raw_text, file_path = "", input_data.get("url"), input_data.get("text"), input_data.get("file_path")

    if url:
        text = fetch_article_text(url)
    elif raw_text:
        text = raw_text[:3000]
    elif file_path:
        if file_path.lower().endswith(".pdf"):
            text = extract_pdf_text(file_path)
        elif file_path.lower().endswith(".docx"):
            text = extract_docx_text(file_path)
        else:
            text = "Unsupported file format."
    else:
        text = "No valid input provided."

    analysis = classify_article(text)
    bias_result = detect_bias(text)

    report = {
        "article_link": url if url else "N/A",
        "credibility_score": analysis["credibility_score"],
        "summary": analysis["summary"],
        "source_analysis": f"Automated classification. Bias: {bias_result['bias']} ({bias_result['confidence']})",
        "corroborating_sources": build_corroborating_sources(text),
        "recommendation": analysis["recommendation"],
        "bias": bias_result["bias"],
        "bias_confidence": bias_result["confidence"],
        "explanation": analysis.get("explanation", [])
    }

    report_id = len(db)  # ID for PDF export
    db.insert(report)
    update_source_stats(url if url else "N/A", analysis["credibility_score"])
    report["id"] = report_id
    return report
