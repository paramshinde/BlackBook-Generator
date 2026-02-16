import json
from pathlib import Path


class TemplateService:
    def __init__(self, templates_json_path: str):
        self.templates_json_path = Path(templates_json_path)

    def _load_raw(self):
        if not self.templates_json_path.exists():
            return []
        with self.templates_json_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_templates(self):
        templates = []
        for item in self._load_raw():
            templates.append(
                {
                    "id": item.get("file"),
                    "name": item.get("name"),
                    "file": item.get("file"),
                    "old_details": item.get("old_details", {}),
                }
            )
        return templates

    def get_template(self, template_id: str):
        for item in self._load_raw():
            if item.get("file") == template_id or item.get("name") == template_id:
                return item
        return None
