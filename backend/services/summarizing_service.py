from ..ml.llm import llm_client
from ..core.config import settings

def summarize_text(text: str, max_tokens: int = settings.MAX_TOKENS):
    response = llm_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": text}],
        max_tokens=int(max_tokens),
        top_p=0.95,
        temperature=0.75
    )
    return response.choices[0].message.content
