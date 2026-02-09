from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from ..core.config import settings

tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL_PATH)
device = "cpu"

llm_model = AutoModelForCausalLM.from_pretrained(
    settings.LLM_MODEL_PATH,
    torch_dtype=torch.float32
)
