import requests

url = "http://127.0.0.1:5000/generate"

payload = {
    "priority": "medium",
    "prompt": "write python code for sum of 2 numbers."
}

response = requests.post(
    url,
    json=payload
)
print (response.json())

