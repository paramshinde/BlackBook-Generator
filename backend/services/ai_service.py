import json
import re

import google.generativeai as genai

from config import GEMINI_MODEL, GOOGLE_API_KEY

DOC_KEYS = [
    "doc_introduction",
    "doc_objective",
    "doc_scope",
    "doc_techstack",
    "doc_feasibility",
    "doc_system_features",
    "doc_modules",
    "doc_usecase",
    "doc_advantage",
    "doc_hardware_req",
    "doc_software_req",
]


class AIService:
    def __init__(self):
        self.enabled = bool(GOOGLE_API_KEY)
        if self.enabled:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                GEMINI_MODEL,
                generation_config={"response_mime_type": "application/json"},
            )

    def _fallback(self, project_title: str):
        return {
            key: f"{project_title} - {key.replace('doc_', '').replace('_', ' ').title()} content draft."
            for key in DOC_KEYS
        }

    def _parse_json(self, raw_text: str):
        cleaned = (raw_text or "{}").strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()
        return json.loads(cleaned)

    def generate_documentation(self, project_title: str):
        if not project_title:
            raise ValueError("project_title is required")

        if not self.enabled:
            return self._fallback(project_title)

        prompt = f"""
You are an expert academic writer.
Generate complete project documentation for project title: {project_title}.
Return ONLY JSON with keys exactly: {DOC_KEYS}
Each key should contain structured academic paragraphs.
"""

        response = self.model.generate_content(prompt)
        raw = getattr(response, "text", "{}")

        try:
            data = self._parse_json(raw)
        except Exception:
            return self._fallback(project_title)

        for key in DOC_KEYS:
            if key not in data or not str(data.get(key, "")).strip():
                data[key] = self._fallback(project_title)[key]

        return data
