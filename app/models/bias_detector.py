import re

# A small list of emotional / biased words (expand as needed)
BIAS_WORDS = [
    "shocking", "unbelievable", "disaster", "miracle", "outrage", "scandal",
    "furious", "explosive", "fake", "lie", "propaganda", "corrupt", "evil",
    "heroic", "traitor", "patriot", "biased"
]

def analyze_bias(text: str):
    """
    Simple bias detection:
    - Score = ratio of biased words / total words
    - Highlight biased words in text
    Returns dict with score, label, explanations, highlighted_text
    """

    words = text.split()
    total = len(words)
    bias_hits = 0
    explanations = []
    highlighted_words = []

    highlighted_text_parts = []

    for w in words:
        clean = re.sub(r"[^\w]", "", w).lower()
        if clean in BIAS_WORDS:
            bias_hits += 1
            explanations.append(f"Found biased/emotional word: '{clean}'")
            highlighted_text_parts.append(f"<span class='highlight'>{w}</span>")
            highlighted_words.append(clean)
        else:
            highlighted_text_parts.append(w)

    score = bias_hits / total if total > 0 else 0.0

    if score < 0.05:
        label = "Neutral"
    elif score < 0.15:
        label = "Mixed"
    else:
        label = "Biased"

    return {
        "score": round(score, 2),
        "label": label,
        "explanations": explanations,
        "highlighted_text": " ".join(highlighted_text_parts),
        "highlighted_words": highlighted_words
    }
