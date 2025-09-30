# 📘 Factulist – Fake News & Bias Detector  

> **Clarity in a World of Noise.**  
Factulist is a deep-learning powered application that helps users detect **fake news**, **bias**, and **credibility of sources**.  
It combines NLP models with a clean Bootstrap frontend, explainability features, and exportable reports – designed as both a **class project** and an **entrepreneurship MVP**.  

---

## 🚀 Features  

✅ **Multi-Input Support** – analyze articles via:  
- 🔗 URL (auto-scrapes content)  
- 📝 Raw text  
- 📂 File upload (PDF, DOCX)  

✅ **Deep Learning Backend**  
- Hugging Face transformer models for **fake news classification**  
- Sentiment proxy for **political bias detection**  
- Lightweight **explainability** (top tokens influencing classification)  

✅ **Analytics & History**  
- Credibility timeline with **charts** (Chart.js)  
- Bias distribution visualization  
- History of all reports (stored in TinyDB)  

✅ **Source Credibility Leaderboard**  
- Tracks domains across reports  
- Shows total reports + breakdown by credibility  
- Bar and stacked charts with **pagination**  

✅ **Export & Sharing**  
- Export reports or sources as **CSV**  
- Download individual reports as **PDF**  

✅ **Polished Frontend**  
- Built with **Flask + Bootstrap 5 + Chart.js**  
- Clean responsive UI with **progress bars, badges, and charts**  

---

## 📂 Project Structure  

```
Factulist/
│── run.py                      # Flask entry point
│── requirements.txt             # Dependencies
│
├── app/
│   ├── __init__.py
│   ├── routes.py                # Routes (/, /check, /history, /sources, exports)
│   │
│   ├── models/                  # Deep learning models
│   │   ├── credibility_checker.py
│   │   └── bias_detector.py
│   │
│   ├── services/                # Business logic
│   │   └── report_generator.py
│   │
│   ├── templates/               # Frontend
│   │   ├── report.html          # Main analyzer
│   │   ├── history.html         # History + charts
│   │   └── sources.html         # Source leaderboard
│   │
│   ├── static/                  # CSS/JS assets (if any)
│   └── uploads/                 # Uploaded PDF/DOCX files
│
├── data/
│   ├── reports.json             # Report history (TinyDB)
│   └── sources.json             # Source stats (TinyDB)
```

---

## ⚙️ Installation & Setup  

### 1. Clone Repo  
```bash
git clone https://github.com/<DhairyaKukadia>/factulist.git
cd factulist
```

### 2. Create Virtual Environment  
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows (PowerShell)
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Run App  
```bash
python run.py
```
Visit 👉 `http://127.0.0.1:5000/`  

---

## 📊 Usage  

- **Home (`/`)** → Paste URL, raw text, or upload PDF/DOCX → get report.  
- **History (`/history`)** → See past reports with pie/bar charts.  
- **Sources (`/sources`)** → Domain leaderboard + credibility breakdown.  
- **Exports** →  
  - `/export/reports/csv` → all reports as CSV  
  - `/export/sources/csv` → all sources as CSV  
  - `/export/report/<id>/pdf` → download a single report as PDF  

---

## 📦 Dependencies  

Main stack:  
- **Flask** – web framework  
- **Requests + BeautifulSoup4** – scraping  
- **Transformers + Torch** – deep learning models  
- **pdfplumber + python-docx** – file parsing  
- **TinyDB** – lightweight JSON database  
- **Chart.js** – interactive charts  
- **Bootstrap 5** – UI  
- **pandas** – CSV export  
- **fpdf** – PDF export  

See `requirements.txt` for full list.  

---

## 🧠 Models  

- **Fake News Detection** → `mrm8488/bert-tiny-finetuned-fake-news-detection` (fallback: sentiment model)  
- **Bias Proxy** → `distilbert-base-uncased-finetuned-sst-2-english`  

---

## 📌 Future Enhancements  

- [ ] **Authentication** → user-specific histories & roles  
- [ ] **Fact-checking APIs** → integrate with external sources  
- [ ] **Browser Extension** → fact-check directly while browsing  
- [ ] **Advanced XAI** → LIME/SHAP for better explainability  

---

## 👨‍💻 Authors  

- **Dhairya Kukadia** – BSc Data Science, Navratna University, Vadodara  
- Project for **Deep Learning + Entrepreneurship** coursework  

---

## ⚠️ Disclaimer  

Factulist is an MVP built for **educational purposes**.  
The models provide **probabilistic estimates**, not absolute truth.  
Always cross-verify important news with trusted sources.  
