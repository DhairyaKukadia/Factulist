from datetime import datetime

def generate_report(text, bias_result, credibility_result):
    """
    Builds a standardized report object for TinyDB + templates.
    Ensures all expected keys are always present.
    """
    report = {
        "title": text[:60] + "..." if len(text) > 60 else (text if text else "Untitled"),
        "bias_score": bias_result.get("score", 0.0),
        "bias_label": bias_result.get("label", "Unknown"),
        "notes": bias_result.get("explanations", []),
        "highlighted_text": bias_result.get("highlighted_text", text),
        "highlighted_words": bias_result.get("highlighted_words", []),
        "highlighted_word_count": len(bias_result.get("highlighted_words", [])),
        "credibility_raw": credibility_result if credibility_result else {},
        "credibility_stars": round(credibility_result.get("score", 0.0) * 5) if credibility_result else 0,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "text": text
    }
    return report
