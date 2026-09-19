import re


# -----------------------------------------
# Limits
# -----------------------------------------

MAX_MESSAGE_LENGTH = 12000
MAX_MESSAGES = 50
MAX_OUTPUT_LENGTH = 20000


# -----------------------------------------
# Patterns
# -----------------------------------------

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{20,}",              # OpenAI-style keys
    r"gsk_[A-Za-z0-9_-]{20,}",             # Groq-style keys
    r"AIza[A-Za-z0-9_-]{20,}",              # Google API keys
    r"hf_[A-Za-z0-9_-]{20,}",              # Hugging Face tokens
    r"AKIA[0-9A-Z]{16}",                   # AWS access key
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(me\s+)?your\s+system\s+prompt",
    r"print\s+(your\s+)?system\s+instructions",
]


# -----------------------------------------
# Input Guardrail
# -----------------------------------------

def validate_input(messages):

    if not isinstance(messages, list):
        return False, "messages must be a list"

    if len(messages) == 0:
        return False, "messages cannot be empty"

    if len(messages) > MAX_MESSAGES:
        return False, "Too many messages in request"

    for message in messages:

        if not isinstance(message, dict):
            return False, "Invalid message format"

        role = message.get("role")
        content = message.get("content")

        if role not in ["system", "user", "assistant"]:
            return False, "Invalid message role"

        if not isinstance(content, str):
            return False, "Message content must be a string"

        if not content.strip():
            return False, "Message content cannot be empty"

        if len(content) > MAX_MESSAGE_LENGTH:
            return False, "Message is too long"

        # Check for exposed API keys/secrets
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, content):
                return False, "Potential API key or secret detected"

        # Check prompt injection attempts
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return False, "Potential prompt injection detected"

    return True, None


# -----------------------------------------
# Output Guardrail
# -----------------------------------------

def validate_output(content):

    if not content:
        return False, "Model returned empty response"

    if not isinstance(content, str):
        return False, "Invalid model response"

    if len(content) > MAX_OUTPUT_LENGTH:
        return False, "Model response is too long"

    # Prevent accidentally returning API keys
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            return False, "Model response contains a potential secret"

    return True, None