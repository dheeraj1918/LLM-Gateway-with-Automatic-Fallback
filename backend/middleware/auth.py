from functools import wraps
from flask import request, jsonify

from backend.services.auth_services import hash_gateway_key
from backend.database.mongodb import gateway_keys_collection


def require_gateway_key(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # -------------------------
        # Get Authorization header
        # -------------------------

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "error": {
                    "message": "Missing API key",
                    "type": "authentication_error"
                }
            }), 401

        # -------------------------
        # Check Bearer format
        # -------------------------

        if not auth_header.startswith("Bearer "):

            return jsonify({
                "error": {
                    "message": "Invalid Authorization header",
                    "type": "authentication_error"
                }
            }), 401

        api_key = auth_header.replace("Bearer ", "", 1).strip()

        if not api_key:

            return jsonify({
                "error": {
                    "message": "Missing API key",
                    "type": "authentication_error"
                }
            }), 401

        # -------------------------
        # Hash incoming key
        # -------------------------

        key_hash = hash_gateway_key(api_key)

        # -------------------------
        # Find key in MongoDB
        # -------------------------

        gateway_key = gateway_keys_collection.find_one({
            "key_hash": key_hash,
            "status": "active"
        })

        if not gateway_key:

            return jsonify({
                "error": {
                    "message": "Invalid or inactive API key",
                    "type": "authentication_error"
                }
            }), 401

        # -------------------------
        # Attach user information
        # -------------------------

        request.gateway_key = gateway_key

        return f(*args, **kwargs)

    return decorated