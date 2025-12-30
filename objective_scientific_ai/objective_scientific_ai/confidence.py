def compute_confidence(evidence_text):
    score = 0

    if "PubmedArticle" in evidence_text:
        score += 0.4
    if "DOI" in evidence_text:
        score += 0.3
    if "Semantic Scholar" or "Abstract" in evidence_text:
        score += 0.3

    return min(score, 1.0)


