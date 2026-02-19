from ..ml.llm import llm_client
from ..core.config import settings

def create_quiz(summary: str, num_questions: int = 5, max_tokens: int = 512):
    prompt = f"Моля, генерирай {num_questions} въпроса на български, базирани на следния текст:\n{summary}"
    response = llm_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        do_sample=True,
        top_p=0.95,
        temperature=0.75
    )
    result_text = response.choices[0].message.content
    questions = [line.strip() for line in result_text.split("\n") if line.strip()]
    return questions
