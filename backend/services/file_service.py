import json
import os
import uuid
from pathlib import Path

from werkzeug.utils import secure_filename


def _safe_unique_filename(filename: str) -> str:
    clean = secure_filename(filename)
    stem, ext = os.path.splitext(clean)
    return f"{stem}_{uuid.uuid4().hex[:10]}{ext}"


def save_uploaded_list(files, target_dir: str):
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    saved = []
    for file_obj in files:
        if not file_obj or not file_obj.filename:
            continue
        final_name = _safe_unique_filename(file_obj.filename)
        abs_path = os.path.join(target_dir, final_name)
        file_obj.save(abs_path)
        saved.append(
            {
                "original_name": file_obj.filename,
                "filename": final_name,
                "path": abs_path,
            }
        )
    return saved


def parse_json_field(raw_value, default):
    if not raw_value:
        return default
    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        return default


def guess_language(filename: str) -> str:
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".php": "php",
        ".html": "html",
        ".css": "css",
        ".sql": "sql",
        ".json": "json",
    }
    ext = os.path.splitext(filename.lower())[1]
    return mapping.get(ext, "text")


def extract_form_payload(form):
    return {
        "selectedTemplate": form.get("selectedTemplate", ""),
        "studentDetails": parse_json_field(form.get("studentDetails"), {}),
        "documentation": parse_json_field(form.get("documentation"), {}),
        "codeFilesMeta": parse_json_field(form.get("codeFilesMeta"), []),
        "screenshotsMeta": parse_json_field(form.get("screenshotsMeta"), []),
        "diagramsMeta": parse_json_field(form.get("diagramsMeta"), []),
        "references": parse_json_field(form.get("references"), []),
        "plagiarism_report_title": form.get("plagiarism_report_title", "Plagiarism Report"),
    }


def validate_student_details(student_details: dict):
    required = ["name", "project", "professor", "guide", "year"]
    missing = [key for key in required if not str(student_details.get(key, "")).strip()]
    return missing


def validate_documentation(documentation: dict):
    expected_keys = [
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
    empty = [key for key in expected_keys if not str(documentation.get(key, "")).strip()]
    return empty
