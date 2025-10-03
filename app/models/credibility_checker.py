import re
import json
import os
from urllib.parse import urlparse
from datetime import datetime

# Load domain reputation file
DOMAIN_REPUTATION_PATH = os.path.join("data", "domain_reputation.json")
if os.path.exists(DOMAIN_REPUTATION_PATH):
    with open(DOMAIN_REPUTATION_PATH, "r", encoding="utf-8") as f:
        DOMAIN_REPUTATION = json.load(f)
else:
    DOMAIN_REPUTATION = {}

# Emotional / unreliable markers
EMOTIONAL_WORDS = [
    "shocking", "unbelievable", "disaster", "miracle", "outrage", "scandal",
    "furious", "explosive", "fake", "lie", "propaganda", "corrupt", "evil",
    "heroic", "traitor", "patriot", "biased"
]


def extract_domain(text_or_url: str | None):
    """Try to extract a domain if the input looks like a URL."""
    if not text_or_url:  # ✅ Guard against None
        return None
    try:
        parsed = urlparse(text_or_url)
        if parsed.netloc:
            return parsed.netloc.replace("www.", "")
    except Exception:
        return None
    return None


def check_references(text: str):
    """Count the number of references/links in the article text."""
    links = re.findall(r"https?://\S+", text)
    return len(links)


def check_emotional_language(text: str):
    """Count emotional markers in the text."""
    count = 0
    words = text.lower().split()
    for w in words:
        if w in EMOTIONAL_WORDS:
            count += 1
    return count


def check_credibility(text: str, source: str | None = None):
    """
    Compute a credibility score for an article.
    Returns a dict with 'score' (0–1), 'domain_score', 'refs_score', 'lang_score'.
    """

    # Domain-based credibility
    domain_score = 0.5  # neutral default
    if source:
        domain = extract_domain(source)
        if domain and domain in DOMAIN_REPUTATION:
            domain_score = DOMAIN_REPUTATION[domain]

    # References / citations
    refs = check_references(text)
    if refs >= 5:
        refs_score = 1.0
    elif refs >= 2:
        refs_score = 0.7
    elif refs == 1:
        refs_score = 0.5
    else:
        refs_score = 0.2

    # Language neutrality
    emotional_count = check_emotional_language(text)
    if emotional_count == 0:
        lang_score = 1.0
    elif emotional_count < 3:
        lang_score = 0.7
    else:
        lang_score = 0.3

    # Weighted average
    final_score = (0.4 * domain_score) + (0.3 * refs_score) + (0.3 * lang_score)

    return {
        "score": round(final_score, 2),
        "domain_score": domain_score,
        "refs_score": refs_score,
        "lang_score": lang_score,
        "refs_found": refs,
        "emotional_words": emotional_count,
        "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
