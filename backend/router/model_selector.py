from backend.config import (
    GROQ_API_KEY,
    GEMINI_API_KEY,
    HUGGINGFACE_API_KEY
)


MODEL_CONFIG = [

    {
        "model": "groq/openai/gpt-oss-20b",
        "provider": "groq",
        "capabilities": [
            "general",
            "coding",
            "simple",
            "fast"
        ]
    },

    {
        "model": "gemini/gemini-3.1-flash-lite",
        "provider": "gemini",
        "capabilities": [
            "general",
            "coding",
            "reasoning",
            "fast"
        ]
    },

    {
        "model": "huggingface/deepseek-ai/DeepSeek-R1",
        "provider": "huggingface",
        "capabilities": [
            "general",
            "coding",
            "reasoning"
        ]
    }
]


PROVIDER_KEYS = {
    "groq": GROQ_API_KEY,
    "gemini": GEMINI_API_KEY,
    "huggingface": HUGGINGFACE_API_KEY
}


def get_available_models():

    available_models = []

    for model in MODEL_CONFIG:

        provider = model["provider"]

        api_key = PROVIDER_KEYS.get(provider)

        if api_key:
            available_models.append(model)

    return available_models