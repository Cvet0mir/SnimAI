import os
from groq import Groq
from ..core.config import settings

llm_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
