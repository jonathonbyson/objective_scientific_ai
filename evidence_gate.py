def sufficient_evidence(text: str, min_chars: int = 800) -> bool:
    return len(text.strip()) >= min_chars
