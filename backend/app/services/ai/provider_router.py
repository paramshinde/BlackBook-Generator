from flask import current_app

from .gemini_provider import GeminiProvider


def get_ai_provider():
    return GeminiProvider(
        api_key=current_app.config.get("GEMINI_API_KEY", ""),
        model_name=current_app.config.get("GEMINI_MODEL", "gemini-2.5-flash-lite"),
    )
