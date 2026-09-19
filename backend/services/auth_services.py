import hashlib
import secrets


def generate_gateway_key():
    """
    Generate a new gateway API key.
    """
    return "gw_live_" + secrets.token_urlsafe(32)


def hash_gateway_key(api_key):
    """
    Hash the gateway key before storing it.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()