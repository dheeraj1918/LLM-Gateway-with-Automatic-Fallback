from .gemini import generate as  gemini_generate
from .huggingface  import generate as huggingface_generate
from .groq import generate as groq_generate

PROVIDERS = {
    "gemini": gemini_generate,
    "huggingface": huggingface_generate,
    "groq": groq_generate,
}