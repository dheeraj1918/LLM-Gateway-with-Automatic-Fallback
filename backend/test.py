import requests
body={
    "model": "auto",
    "messages": [
        {
            "role": "user",
            "content": "pm modi birthday"
        }
    ]
}
res=requests.post("http://127.0.0.1:8000/v1/chat/completions",json=body)
print(res.json())
