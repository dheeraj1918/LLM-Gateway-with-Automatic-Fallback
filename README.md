<p>The fallback mechanism automatically tries another chat model when the current model fails. Models are selected and attempted based on the user's priority level: Low, Medium, or High.</p>

<p>Example:</p>
<p>python</p>

```
import requests

url = "http://127.0.0.1:5000/generate"

payload = {
    "priority": "low",
    "prompt": "write python code for sum of 2 numbers."
}

response = requests.post(
    url,
    json=payload
)
print (response.json())
```
