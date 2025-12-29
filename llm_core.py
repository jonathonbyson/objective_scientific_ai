import os
from openai import OpenAI

NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")
if not NEBIUS_API_KEY:
    raise ValueError("NEBIUS_API_KEY environment variable not set")

client = OpenAI(
    api_key=NEBIUS_API_KEY,
    base_url="https://api.tokenfactory.nebius.com/v1/"
)

def answer_with_constraints(question: str, evidence: str) -> str:
    """
    Generate a concise scientific answer based only on provided evidence
    and list the sources.
    """
    prompt = (
        f"Answer the following scientific question using only reliable scientific evidence:\n\n"
        f"Question: {question}\n\n"
        f"Evidence:\n{evidence}\n\n"
        f"Provide a concise summary and list your sources with links."
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are an objective scientific AI."},
            {"role": "user", "content": prompt}
        ]
    )

    # Access the content attribute of the message object
    return response.choices[0].message.content

