import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "llm_gateway"
GROQ_API_KEY=os.getenv("groq_api")
GEMINI_API_KEY=os.getenv("gemini_api")
HUGGINGFACE_API_KEY=os.getenv("hf_token")