import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("api_key")
API_KEY=api_key
headers={
    "Authorization": f"Bearer {API_KEY}"
}
body = {
    "model": "auto",
    "messages": [
        {
            "role": "user",
            "content": "about india."
        }
    ]
}

res = requests.post(
    "http://127.0.0.1:8000/v1/chat/completions",
    json=body,headers=headers
)

print(res.status_code)
print(res.json())