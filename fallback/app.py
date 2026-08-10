from flask import Flask,request,jsonify
from flask_cors import CORS
from router import generate

app=Flask(__name__)
CORS(app)

@app.route("/generate",methods=["POST"])
def llm():
    data=request.json
    priority=data["priority"]
    prompt=data["prompt"]
    result = generate(priority,prompt)
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)