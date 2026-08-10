from config.config import MODELS
from providers import PROVIDERS

def generate(priority,prompt):
    models=MODELS[priority]
    for model in models:
        provider=model["provider"]
        model_name=model["model"]
        try:
            response=PROVIDERS[provider](
                prompt,model_name
            )
            return {
                "success": True,
                "provider": provider,
                "model": model_name,
                "response": response
            }
        except Exception as e:
            print(f"Error {e}")
            continue
    return {
        "success": False,
        "message": "No model available"
    }
    
