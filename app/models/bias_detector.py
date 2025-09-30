from transformers import pipeline

bias_classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")  # type: ignore

def detect_bias(text: str) -> dict:
    try:
        if not text or text.startswith("Error"):
            return {"bias": "⚖️ Center / Neutral", "confidence": "0.00"}
        result = bias_classifier(text[:512])[0]
        label, score = result["label"].upper(), result["score"]
        if label == "POSITIVE": bias = "⬅️ Left-leaning"
        elif label == "NEGATIVE": bias = "➡️ Right-leaning"
        else: bias = "⚖️ Center / Neutral"
        return {"bias": bias, "confidence": f"{score:.2f}"}
    except Exception as e:
        return {"bias": "Unknown", "confidence": "0.00", "error": str(e)}
