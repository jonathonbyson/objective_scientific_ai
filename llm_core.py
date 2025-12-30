import os
from openai import OpenAI
from validators import validate_evidence
from confidence import compute_confidence

if not os.environ.get("NEBIUS_API_KEY"):
    raise ValueError("NEBIUS_API_KEY environment variable not set")

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.environ["NEBIUS_API_KEY"]
)

def answer_with_constraints(question, evidence):
    if not validate_evidence(evidence):
        return "Sorry — I don’t have enough information to give you a solid conclusion."

    confidence = compute_confidence(evidence)

    prompt = f"""
You are an objective scientific research assistant.

Rules:
- Use ONLY the evidence provided
- Do NOT speculate
- Cite sources explicitly
- If evidence is weak, say so

QUESTION:
{question}

EVIDENCE:
{evidence}

Provide:
1. A concise evidence-based summary
2. Bullet-point conclusions
3. Explicit sources with links
4. A confidence score
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    return response.choices[0].message.content + f"\n\nConfidence score: {confidence:.2f}"
