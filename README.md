## Testing the API

You can test the LLM Gateway locally using the following Python script. Make sure you have the `requests` library installed (`pip install requests`).

```python
import requests

body = {
    "model": "auto",
    "messages": [
        {
            "role": "user",
            "content": "pm modi birthday"
        }
    ]
}

res = requests.post("http://127.0.0.1:8000/v1/chat/completions", json=body)
print(res.json())
```
