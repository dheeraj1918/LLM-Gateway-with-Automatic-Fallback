import os
from litellm import completion
from backend.config import GROQ_API_KEY, GEMINI_API_KEY, HUGGINGFACE_API_KEY

def generate_response(model, messages):
    if model.startswith("groq/"):
        api_key = GROQ_API_KEY

    elif model.startswith("gemini/"):
        api_key = GEMINI_API_KEY
    elif model.startswith("openai/"):
        api_key = HUGGINGFACE_API_KEY

    else:
        api_key = None
    response = completion(
        model=model,
        messages=messages,
        api_key=api_key
    )

    return response