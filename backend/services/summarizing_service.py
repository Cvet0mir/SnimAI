from ..ml.llm import llm_client
from ..core.config import settings

def summarize_text(text: str, max_tokens: int = settings.MAX_TOKENS):
    response = llm_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": text}],
        max_tokens=max_tokens,
        do_sample=True,
        top_p=0.95,
        temperature=0.75
    )
    return response.choices[0].message.content
