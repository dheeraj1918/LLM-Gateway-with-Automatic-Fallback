import os
from dotenv import load_dotenv
import json
load_dotenv()
def get_keys(name):
    value = os.getenv(name, "")
    return [k.strip() for k in value.split(",") if k.strip()]


GEMINI_KEYS = get_keys("gemini_api")
GROQ_KEYS=get_keys("groq_api")
HUGGINGFACE_KEYS=get_keys("huggingface_api")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_FILE = os.path.join(BASE_DIR, "models.json")
with open(MODELS_FILE,"r") as f:
    MODELS=json.load(f)