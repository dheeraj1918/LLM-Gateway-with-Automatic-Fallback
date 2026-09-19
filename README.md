## Testing the API

You can test the LLM Gateway locally using the following Python script.

First, install the requests library:
```python
pip install requests

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

API_KEY = api_key

headers = {
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
    json=body,
    headers=headers
)

print(res.status_code)
print(res.json())
```
## How to Get an API Key

Send a POST request to the following endpoint to generate a Gateway API key:

http://127.0.0.1:8000/v1/auth/generate-key

Example response:
```json
{
    "api_key": "gw_live_n_oM77o6Gr81rkjGhxkbtrC7zHErdhw7qwmIJpvz9bI",
    "message": "Gateway API key created"
}
```
Add the generated API key to your .env file:

api_key=gw_live_n_oM77o6Gr81rkjGhxkbtrC7zHErdhw7qwmIJpvz9bI