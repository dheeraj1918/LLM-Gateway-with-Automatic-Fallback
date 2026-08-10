from .gemini import generate
from .huggingface import generate
from .groq import generate

PROVIDERS = {
    "gemini": generate,
    "huggingface":generate,
    "groq":generate
}