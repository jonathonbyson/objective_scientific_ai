# actionable_summary.py

def generate_actionable_summary(evidence_chunks: list) -> str | None:
    """
    Generates an actionable summary strictly from validated evidence.
    Returns None if evidence is insufficient.
    """

    if not evidence_chunks or len(evidence_chunks) < 2:
        return None

    known_facts = []
    implications = []
    actions = []
    limits = []

    for e in evidence_chunks:
        if "finding" in e:
            known_facts.append(e["finding"])
        if "implication" in e:
            implications.append(e["implication"])
        if "recommendation" in e:
            actions.append(e["recommendation"])
        if "limitation" in e:
            limits.append(e["limitation"])

    if not known_facts or not implications:
        return None

    summary = f"""
**What we know**
- {"; ".join(known_facts)}

**What this means for you**
- {"; ".join(implications)}

**Recommended action**
- {"; ".join(actions) if actions else "No specific action is supported by 
the evidence."}

**When this advice does NOT apply**
- {"; ".join(limits) if limits else "If your situation differs materially 
from the study conditions."}
""".strip()

    return summary

