from huggingface_hub import InferenceClient
from config.config import HUGGINGFACE_KEYS


HF_TOKEN = HUGGINGFACE_KEYS[0]


def generate(prompt, model_name):

    client = InferenceClient(
        api_key=HF_TOKEN,
        provider="auto"
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=512
    )

    return response.choices[0].message.content