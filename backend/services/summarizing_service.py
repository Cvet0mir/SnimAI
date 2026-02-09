from ..ml.llm import llm_model, tokenizer
from ..core.config import settings

def summarize_text(text: str, max_tokens: int = settings.MAX_TOKENS):
    
    inputs = tokenizer(text, return_tensors="pt").to(llm_model.device)
    summary_ids = llm_model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        top_p=0.95,
        temperature=0.75
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

