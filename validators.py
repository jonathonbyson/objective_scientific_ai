def validate_evidence(evidence_text):
    if not evidence_text:
        return False

    if len(evidence_text) < 1000:
        return False

    required_markers = ["Abstract", "Title"]
    return any(marker in evidence_text for marker in required_markers)

