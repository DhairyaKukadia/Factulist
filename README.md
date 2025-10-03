# 📘 Factulist – Fake News & Bias Detector  

> **Clarity in a World of Noise.**  
Factulist is a Flask-based application that helps users detect **bias** and **credibility of sources** in news articles.  
It combines NLP-driven heuristics with a clean Bootstrap frontend, explainability highlights, and exportable reports – designed as both a **class project** and a **practical MVP**.  

---

## 🚀 Features  

✅ **Multi-Input Support** – analyze articles via:  
- 🔗 URL (auto-scrapes content with newspaper3k)  
- 📝 Raw text  
- 📂 File upload (`.txt` supported, PDF/DOCX planned)  

✅ **Bias Detection**  
- Highlights biased/emotional words  
- Labels as **Neutral / Mixed / Biased**  
- Quick notes with detected terms  

✅ **Credibility Analysis**  
- Domain reputation lookup (`domain_reputation.json`)  
- Reference richness (number of external links)  
- Language neutrality (emotional vs neutral tone)  
- Visual bar chart breakdown (Chart.js)  

✅ **Analytics & History**  
- Stores last 10 reports in **TinyDB** (`data/reports.json`)  
- History table with bias, credibility stars, highlights count, and date  

✅ **Comparison Mode**  
- Compare two articles side by side  
- Radar chart visualization for bias/credibility components  

✅ **Export & Sharing**  
- Download the latest report as **PDF**  
- (Upcoming) Export history as **CSV**  

✅ **Polished Frontend**  
- Built with **Flask + Bootstrap 5 + Chart.js**  
- Responsive UI with **badges, charts, and highlights**  

---

## 📂 Project Structure  

Factulist/
│── run.py                      # Flask entry point
│── requirements.txt            # Dependencies
│── README.md                   # Documentation
│
├── app/
│ ├── routes.py                 # Routes (home, history, compare, about, export)
│ │
│ ├── models/                   # Bias & credibility logic
│ │ ├── credibility_checker.py
│ │ └── bias_detector.py
│ │
│ ├── services/                 # Report builder
│ │ └── report_generator.py
│ │
│ ├── templates/                # Frontend (Jinja + Bootstrap)
│ │ ├── base.html               # Layout + navbar
│ │ ├── index.html              # Input form
│ │ ├── report.html             # Analysis results + chart
│ │ ├── history.html            # Past reports
│ │ ├── compare.html            # Side-by-side comparison + radar chart
│ │ └── about.html              # About/FAQ
│ │
│ ├── static/                   # CSS/JS assets
│ │ └── style.css
│ │
│ └── uploads/                  # Uploaded files (txt for now)
│
├── data/
│ └── reports.json              # TinyDB storage for history

---

## ⚙️ Installation & Setup  

### 1. Clone Repo  

git clone https://github.com/<DhairyaKukadia>/Factulist.git
cd Factulist

### 2. Create Virtual Environment

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows (PowerShell)

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run App

python run.py
Visit 👉 http://127.0.0.1:5000/

### 📊 Usage
**Home** (/) → Paste URL, raw text, or upload .txt → get report.
**Report** (/report) → Shows bias, credibility, highlights, breakdown chart.
**History** (/history) → Last 10 reports with bias/credibility preview.
**Compare** (/compare) → Two articles side by side with radar chart.
**Export** (/export/latest) → Download the latest report as PDF.

### 📦 Dependencies

Main stack:

**Flask** – web framework
**TinyDB** – lightweight JSON database
**newspaper3k** – URL scraping
**lxml_html_clean** – required for newspaper3k
**reportlab** – PDF export
**Chart.js** – interactive charts (CDN)
**Bootstrap 5** – responsive UI

### See requirements.txt for exact versions.

📌 Future Enhancements
 Export history as CSV/Excel

 PDF/DOCX upload support

 Source credibility leaderboard

 User accounts for persistent history

 SHAP/LIME for advanced explainability

 Browser extension integration

👨‍💻 Author
Dhairya Kukadia – BSc Data Science, Navratna University, Vadodara

Project for Deep Learning + Entrepreneurship coursework

⚠️ Disclaimer
Factulist is a project built for educational purposes.
The results are heuristic-based indicators, not absolute truth.
Always cross-verify important news with trusted sources.


---

This gives you the **same polished style** as the one you uploaded, but tailored exactly to your current project capabilities.  

👉 Do you want me to also create a **badged header (with shields.io)** at the top (like “Built with Flask”, “Python 3.10+”, “License: MIT”)? That makes it look even more GitHub-ready.
