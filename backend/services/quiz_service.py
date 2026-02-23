from ..ml.llm import llm_client
import json
import re

def create_quiz(summary: str, num_questions: int = 5, max_tokens: int = 512):

    if not summary or len(summary.strip()) < 20:
        return []

    prompt = (
        f"Генерирай {num_questions} въпроса на български, базирани на следния текст:\n\n"
        f"{summary}\n\n"
        "Върни САМО валиден JSON списък.\n"
        "Не използвай markdown.\n"
        "Формат:\n"
        "[\n"
        '  {"question": "...", "correct_answer": "..."}\n'
        "]"
    )

    response = llm_client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=int(max_tokens),
        top_p=0.95,
        temperature=0.75
    )

    result_text = response.choices[0].message.content.strip()
    result_text = re.sub(r"```json", "", result_text)
    result_text = re.sub(r"```", "", result_text).strip()

    try:
        quiz_data = json.loads(result_text)
    except json.JSONDecodeError:
        print("AI returned invalid JSON:")
        print(result_text)
        return []

    if not isinstance(quiz_data, list):
        return []

    cleaned_quiz = []

    for item in quiz_data:
        if (
            isinstance(item, dict)
            and "question" in item
            and "correct_answer" in item
            and item["question"]
            and item["correct_answer"]
        ):
            cleaned_quiz.append({
                "question": item["question"],
                "correct_answer": item["correct_answer"]
            })

    return cleaned_quiz

