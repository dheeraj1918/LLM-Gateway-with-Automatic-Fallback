from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
from config.config import GEMINI_KEYS

os.environ["GOOGLE_API_KEY"]=GEMINI_KEYS[0]


def generate(prompt, model_name):

    model = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=1.0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )
    message=[("human",prompt)]
    response=model.invoke(message)
    return response.text
