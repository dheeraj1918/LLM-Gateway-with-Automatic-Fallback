from backend.router.classifier import classifier_query
from backend.router.model_selector import get_available_models


def route_query(query):

    classification = classifier_query(query)

    task = classification["task"]
    complexity = classification["complexity"]

    available_models = get_available_models()

    if not available_models:
        raise RuntimeError(
            "No LLM provider API keys are configured"
        )

    matching_models = []

    for model in available_models:

        if task in model["capabilities"]:
            matching_models.append(model)

    if not matching_models:
        raise RuntimeError(
            f"No available model supports task: {task}"
        )

    return {
        "task": task,
        "complexity": complexity,
        "models": matching_models
    }