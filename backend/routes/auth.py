from flask import Blueprint, jsonify

from backend.services.auth_services import (
    generate_gateway_key,
    hash_gateway_key
)

from backend.database.mongodb import gateway_keys_collection


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/generate-key")
def generate_key():

    api_key = generate_gateway_key()

    key_hash = hash_gateway_key(api_key)

    gateway_keys_collection.insert_one({
        "key_hash": key_hash,
        "status": "active"
    })

    return jsonify({
        "message": "Gateway API key created",
        "api_key": api_key
    })