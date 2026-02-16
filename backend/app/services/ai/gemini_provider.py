import json

from ...utils.text_cleaning import to_academic_tone_fallback
from .prompts import DIAGRAM_GENERATION_PROMPT, SECTION_IMPROVEMENT_PROMPT

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None

from .provider_base import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.enabled = bool(api_key and genai)
        if self.enabled:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)

    def _generate_json(self, prompt: str) -> dict:
        if not self.enabled:
            return {}
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "{}") or "{}"
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}

    def improve_section(self, section_title: str, content: str, target_words: int) -> dict:
        if not self.enabled:
            return {
                "improved_text": to_academic_tone_fallback(content),
                "changes_summary": "Fallback rewrite applied because Gemini is not configured.",
            }
        prompt = (
            f"{SECTION_IMPROVEMENT_PROMPT}\nSection Title: {section_title}\n"
            f"Target words: {target_words}\nInput:\n{content}"
        )
        parsed = self._generate_json(prompt)
        return {
            "improved_text": parsed.get("improved_text", to_academic_tone_fallback(content)),
            "changes_summary": parsed.get("changes_summary", "Academic rewrite generated."),
        }

    def generate_diagram_spec(self, project_title: str) -> dict:
        if not self.enabled:
            return {
                "er": {"entities": ["Student", "Project"]},
                "class": {"classes": ["ProjectService", "ExportService"]},
                "sequence": {"actors": ["Student", "System"]},
                "usecase": {"actors": ["Student", "Guide"]},
            }
        prompt = DIAGRAM_GENERATION_PROMPT.format(project_title=project_title)
        return self._generate_json(prompt)
