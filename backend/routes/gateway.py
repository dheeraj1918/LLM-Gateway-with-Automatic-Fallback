from flask import Blueprint, request, jsonify

from backend.router.router import route_query
from backend.services.llm_service import generate_response
from backend.middleware.auth import require_gateway_key
from backend.services.guardrail_service import (
    validate_input,
    validate_output
)


gateway_bp = Blueprint("gateway", __name__)


@gateway_bp.post("/chat/completions")
@require_gateway_key
def chat_completions():

    # =========================================
    # READ REQUEST
    # =========================================

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": {
                "message": "Invalid request body",
                "type": "invalid_request_error"
            }
        }), 400


    # =========================================
    # GET MESSAGES
    # =========================================

    messages = data.get("messages")

    if not messages:
        return jsonify({
            "error": {
                "message": "messages is required",
                "type": "invalid_request_error"
            }
        }), 400


    # =========================================
    # INPUT GUARDRAILS
    # =========================================

    valid, guardrail_error = validate_input(messages)

    if not valid:

        print("\n========== INPUT GUARDRAIL BLOCKED ==========")
        print("Reason:", guardrail_error)
        print("=============================================\n")

        return jsonify({
            "error": {
                "message": guardrail_error,
                "type": "guardrail_violation"
            }
        }), 400


    # =========================================
    # GET LATEST USER MESSAGE
    # =========================================

    user_query = messages[-1]["content"]


    # =========================================
    # INTELLIGENT ROUTING
    # =========================================

    try:

        routing = route_query(user_query)

    except Exception as e:

        print("\n========== ROUTING ERROR ==========")
        print("Error:", str(e))
        print("===================================\n")

        return jsonify({
            "error": {
                "message": "Unable to route request",
                "type": "routing_error"
            }
        }), 503


    models = routing["models"]


    # =========================================
    # ROUTING LOGS
    # =========================================

    print("\n========== ROUTING ==========")

    print("Query:", user_query)

    print("Task:", routing["task"])

    print("Complexity:", routing["complexity"])

    print("Candidate models:")

    for model in models:
        print(" -", model["model"])

    print("=============================\n")


    # =========================================
    # MODEL FALLBACK
    # =========================================

    response = None

    successful_model = None

    response_content = None


    for model in models:

        try:

            print("Trying:", model["model"])


            # ---------------------------------
            # CALL LLM
            # ---------------------------------

            response = generate_response(
                model=model["model"],
                messages=messages
            )


            # ---------------------------------
            # GET RESPONSE CONTENT
            # ---------------------------------

            response_content = (
                response
                .choices[0]
                .message
                .content
            )


            # ---------------------------------
            # OUTPUT GUARDRAILS
            # ---------------------------------

            valid, guardrail_error = validate_output(
                response_content
            )


            if not valid:

                print("\n========== OUTPUT GUARDRAIL ==========")

                print(
                    "Model:",
                    model["model"]
                )

                print(
                    "Reason:",
                    guardrail_error
                )

                print(
                    "Trying next model..."
                )

                print("======================================\n")


                # Treat guardrail failure
                # as model failure
                response = None
                response_content = None

                continue


            # ---------------------------------
            # SUCCESS
            # ---------------------------------

            successful_model = model


            print("\nSUCCESS:", model["model"])

            print("=============================")

            print(response_content)

            print("=============================\n")


            break


        # -------------------------------------
        # MODEL ERROR
        # -------------------------------------

        except Exception as e:

            print("\n========== MODEL FAILED ==========")

            print(
                "Model:",
                model["model"]
            )

            print(
                "Error:",
                str(e)
            )

            print(
                "Trying next model..."
            )

            print("=================================\n")


            response = None

            response_content = None

            continue


    # =========================================
    # ALL MODELS FAILED
    # =========================================

    if response is None or successful_model is None:

        return jsonify({
            "error": {
                "message": "All available models failed",
                "type": "llm_unavailable"
            }
        }), 503


    # =========================================
    # FINAL RESPONSE
    # =========================================

    return jsonify({

        "id": response.id,

        "object": "chat.completion",

        "model": successful_model["model"],

        "provider": successful_model["provider"],


        # -------------------------------------
        # ROUTING INFORMATION
        # -------------------------------------

        "routing": {

            "task": routing["task"],

            "complexity": routing["complexity"]

        },


        # -------------------------------------
        # RESPONSE
        # -------------------------------------

        "choices": [

            {

                "index": 0,

                "message": {

                    "role": response
                    .choices[0]
                    .message
                    .role,

                    "content": response_content

                },

                "finish_reason": response
                .choices[0]
                .finish_reason

            }

        ]

    })