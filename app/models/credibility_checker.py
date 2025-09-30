from transformers import pipeline

_FAKE_MODEL_ID = "mrm8488/bert-tiny-finetuned-fake-news-detection"
_SENTI_MODEL_ID = "distilbert-base-uncased-finetuned-sst-2-english"

def _load_pipelines():
    try:
        clf = pipeline("text-classification", model=_FAKE_MODEL_ID)  # type: ignore
        fallback = pipeline("sentiment-analysis", model=_SENTI_MODEL_ID)  # type: ignore
        return clf, fallback
    except Exception:
        fallback = pipeline("sentiment-analysis", model=_SENTI_MODEL_ID)  # type: ignore
        return None, fallback

_classifier, _sentiment = _load_pipelines()

def _label_from_sentiment(text: str):
    res = _sentiment(text[:512])[0]
    lab, score = res["label"], res["score"]
    if lab.upper() == "NEGATIVE":
        return "🟠 Misleading", f"Sentiment NEGATIVE ({score:.2f}); proxy.", "Share with Caution"
    else:
        return "✅ Verified", f"Sentiment POSITIVE ({score:.2f}); proxy.", "Safe to Share"

def classify_article(text: str) -> dict:
    if not text or text.startswith("Error"):
        return {"credibility_score": "🟡 Mostly True", "summary": "Parse error", "recommendation": "Caution", "explanation": []}

    if _classifier:
        try:
            result = _classifier(text[:512])[0]
            label, score = result["label"].upper(), result["score"]
            if "FAKE" in label:
                cred, summary, reco = "❌ False", f"Model: FAKE ({score:.2f})", "Do Not Share"
            else:
                cred, summary, reco = "✅ Verified", f"Model: REAL ({score:.2f})", "Safe to Share"
        except Exception:
            cred, summary, reco = _label_from_sentiment(text)
    else:
        cred, summary, reco = _label_from_sentiment(text)

    explanation, seen = [], set()
    for w in [w for w in text.split()[:100] if w.isalpha()]:
        if w.lower() in seen: continue
        seen.add(w.lower())
        try:
            res = (_classifier or _sentiment)(w)[0]
            explanation.append((w, float(res["score"]), str(res["label"])))
        except: continue
    explanation.sort(key=lambda x: x[1], reverse=True)
    return {"credibility_score": cred, "summary": summary, "recommendation": reco, "explanation": explanation[:5]}
