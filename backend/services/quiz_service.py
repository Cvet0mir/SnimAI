from ..ml.llm import llm_model, tokenizer
from ..core.config import settings

def create_quiz(summary: str, num_questions: int = 5, max_tokens: int = settings.MAX_TOKENS) -> list:

    prompt = f"Generate {num_questions} questions based on the following text:\n{summary}"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(llm_model.device)
    output_ids = llm_model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        top_p=0.95,
        temperature=0.75
    )
    result_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    questions = [line.strip() for line in result_text.split("\n") if line.strip()]
    return questions
