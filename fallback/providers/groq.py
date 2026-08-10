from langchain_groq import ChatGroq
from config.config import GROQ_KEYS
import os

os.environ["GROQ_API_KEY"]=GROQ_KEYS[0]
def generate(prompt, model_name):
    llm = ChatGroq(
    model=model_name,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
    )
    messages = [(
        "system",
        "You are a helpful AI assistant ",
    ),("human", prompt),]
    ai_msg = llm.invoke(messages)
    return ai_msg.content
    
