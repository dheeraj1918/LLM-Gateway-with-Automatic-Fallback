from flask import Blueprint, request, jsonify

from backend.router.router import route_query
from backend.services.llm_service import generate_response


gateway_bp = Blueprint("gateway", __name__)


@gateway_bp.post("/chat/completions")
def chat_completions():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "message": "Invalid request body",
                "type": "invalid_request_error"
            }
        }), 400

    messages = data.get("messages")

    if not messages:
        return jsonify({
            "error": {
                "message": "messages is required",
                "type": "invalid_request_error"
            }
        }), 400

    # Get latest user message
    user_query = messages[-1]["content"]

    # -----------------------------
    # Intelligent routing
    # -----------------------------

    routing = route_query(user_query)

    models = routing["models"]

    print("\n========== ROUTING ==========")
    print("Query:", user_query)
    print("Task:", routing["task"])
    print("Complexity:", routing["complexity"])
    print("Candidate models:")

    for model in models:
        print(" -", model["model"])

    print("=============================\n")

    # -----------------------------
    # Try models with fallback
    # -----------------------------

    response = None
    successful_model = None

    for model in models:

        try:

            print("Trying:", model["model"])

            response = generate_response(
                model=model["model"],
                messages=messages
            )

            successful_model = model
            
            print("SUCCESS:", model["model"])
            print("=============================\n")
            print(response.choices[0].message.content)

            break

        except Exception as e:

            print("FAILED:", model["model"])
            print("Error:", str(e))

            continue

    # -----------------------------
    # All models failed
    # -----------------------------

    if response is None:

        return jsonify({
            "error": {
                "message": "All available models failed",
                "type": "llm_unavailable"
            }
        }), 503

    # -----------------------------
    # Return response
    # -----------------------------

    return jsonify({

        "id": response.id,

        "object": "chat.completion",

        "model": successful_model["model"],

        "provider": successful_model["provider"],

        "routing": {
            "task": routing["task"],
            "complexity": routing["complexity"]
        },

        "choices": [
            {
                "index": 0,

                "message": {
                    "role": response.choices[0].message.role,
                    "content": response.choices[0].message.content
                },

                "finish_reason": response.choices[0].finish_reason
            }
        ]
    })