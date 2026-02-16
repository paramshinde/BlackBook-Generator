import os
import re
import time
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

from config import BASE_DIR, GENERATED_DIR, TEMPLATES_JSON_PATH, UPLOAD_DIR
from services.ai_service import AIService
from services.document_service import generate_document
from services.file_service import (
    extract_form_payload,
    guess_language,
    save_uploaded_list,
    validate_documentation,
    validate_student_details,
)
from services.preview_service import render_preview_html
from services.template_service import TemplateService

app = Flask(__name__)
CORS(app)

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(GENERATED_DIR).mkdir(parents=True, exist_ok=True)

template_service = TemplateService(TEMPLATES_JSON_PATH)
ai_service = AIService()
HF_ROUTER_BASE_URL = "https://router.huggingface.co/hf-inference/models"
HF_DIAGRAM_MODEL_IDS = [
    # Requested legacy ID.
    "runwayml/stable-diffusion-v1-5",
    # Current canonical ID on Hugging Face Hub.
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    # Fallback model currently supported by HF Inference Router.
    "stabilityai/stable-diffusion-xl-base-1.0",
]
HF_PLANTUML_MODEL = "HuggingFaceH4/zephyr-7b-beta"
KROKI_PLANTUML_PNG_URL = "https://kroki.io/plantuml/png"


def _safe_diagram_slug(diagram_type: str) -> str:
    """
    Convert a diagram label into a filesystem-safe slug for filenames.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", diagram_type.strip().lower())
    return cleaned.strip("_") or "diagram"


def _build_plantuml_prompt(project_title: str, diagram_type: str) -> str:
    """
    Build a strict prompt that asks the model to return only valid PlantUML.
    """
    return (
        "Generate valid PlantUML code ONLY (including @startuml and @enduml)\n"
        f'for a {diagram_type} for a final year engineering project titled "{project_title}".\n\n'
        "Rules:\n"
        "- Academic style\n"
        "- Clean UML\n"
        "- Proper entities, actors, relationships\n"
        "- No explanation text\n"
        "- Return only PlantUML code"
    )


def _extract_text_from_hf_response(payload) -> str:
    """
    Normalize HF response payload into plain text.
    """
    if isinstance(payload, str):
        return payload
    if isinstance(payload, list):
        parts = []
        for item in payload:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("generated_text") or item.get("text") or item.get("summary_text") or ""))
        return "\n".join(p for p in parts if p).strip()
    if isinstance(payload, dict):
        return str(
            payload.get("generated_text")
            or payload.get("text")
            or payload.get("output_text")
            or payload.get("answer")
            or ""
        ).strip()
    return ""


def _extract_plantuml_block(text: str) -> str:
    """
    Extract only the PlantUML block from model output.
    """
    if not text:
        raise ValueError("Empty response from Hugging Face model.")

    start = text.find("@startuml")
    end = text.find("@enduml")
    if start == -1 or end == -1 or end < start:
        raise ValueError("Model did not return valid PlantUML with @startuml and @enduml.")

    return text[start : end + len("@enduml")].strip()


def _is_plantuml_suitable_for_type(plantuml_code: str, diagram_type: str) -> bool:
    """
    Validate whether generated PlantUML resembles the requested diagram type.
    """
    code = (plantuml_code or "").lower()
    # Ignore title/comment lines so keyword checks do not get false positives.
    structural = "\n".join(
        line for line in code.splitlines() if not line.strip().startswith("title ")
    )
    dtype = (diagram_type or "").lower()

    # Reject common generic use-case shape for non use-case requests.
    generic_usecase = (
        "actor " in structural
        and "usecase " in structural
        and "rectangle system" in structural
    )
    if generic_usecase and "use case" not in dtype:
        return False

    if "event table" in dtype:
        return bool(re.search(r"^\s*class\s+eventtable\b", structural, re.MULTILINE))
    if "entity relationship" in dtype or dtype.strip() == "er":
        return bool(re.search(r"^\s*entity\s+[a-z0-9_]+", structural, re.MULTILINE))
    if "class" in dtype:
        return bool(re.search(r"^\s*class\s+[a-z0-9_]+", structural, re.MULTILINE))
    if "activity" in dtype:
        return "start" in structural and "stop" in structural
    if "use case" in dtype:
        return "usecase " in structural and "actor " in structural
    if "sequence" in dtype:
        return "->" in structural and "participant " in structural
    if "component" in dtype:
        return "[" in structural and "]" in structural
    if "deployment" in dtype:
        return bool(re.search(r"^\s*node\s+", structural, re.MULTILINE))
    if "database" in dtype:
        return bool(
            re.search(r"^\s*database\s+", structural, re.MULTILINE)
            or re.search(r"^\s*entity\s+[a-z0-9_]+", structural, re.MULTILINE)
        )
    return True


def _fallback_plantuml(project_title: str, diagram_type: str) -> str:
    """
    Fallback PlantUML when model output is unavailable (e.g., model 404).
    Keeps the HF->PlantUML->Kroki flow operational.
    """
    safe_title = (project_title or "Project").replace('"', "'")
    safe_type = (diagram_type or "UML Diagram").replace('"', "'").lower()

    if "event table" in safe_type:
        return (
            "@startuml\n"
            f"title Event Table - {safe_title}\n"
            "class EventTable {\n"
            "  +Event: string\n"
            "  +Trigger: string\n"
            "  +Input: string\n"
            "  +Output: string\n"
            "}\n"
            "note right of EventTable\n"
            "Login | Credentials | User/Pass | Session\n"
            "Add Entry | Form Submit | Student Data | Record\n"
            "Generate Report | Export Click | Filters | Report\n"
            "end note\n"
            "@enduml"
        )

    if "entity relationship" in safe_type or "er" == safe_type:
        return (
            "@startuml\n"
            f"title Entity Relationship Diagram - {safe_title}\n"
            "entity STUDENT {\n"
            "  *student_id : int\n"
            "  --\n"
            "  name : string\n"
            "  email : string\n"
            "}\n"
            "entity SUBJECT {\n"
            "  *subject_id : int\n"
            "  subject_name : string\n"
            "}\n"
            "entity ATTENDANCE {\n"
            "  *attendance_id : int\n"
            "  date : date\n"
            "  status : string\n"
            "}\n"
            "STUDENT ||--o{ ATTENDANCE : marks\n"
            "SUBJECT ||--o{ ATTENDANCE : for\n"
            "@enduml"
        )

    if "class" in safe_type:
        return (
            "@startuml\n"
            f"title Class Diagram - {safe_title}\n"
            "class User {\n"
            "  +id: int\n"
            "  +name: string\n"
            "  +login()\n"
            "}\n"
            "class Student {\n"
            "  +rollNo: string\n"
            "  +viewReport()\n"
            "}\n"
            "class Admin {\n"
            "  +uploadData()\n"
            "  +generateReport()\n"
            "}\n"
            "class AttendanceService {\n"
            "  +markAttendance()\n"
            "  +getAttendance()\n"
            "}\n"
            "User <|-- Student\n"
            "User <|-- Admin\n"
            "Admin --> AttendanceService\n"
            "Student --> AttendanceService\n"
            "@enduml"
        )

    if "activity" in safe_type:
        return (
            "@startuml\n"
            f"title Activity Diagram - {safe_title}\n"
            "start\n"
            ":User Login;\n"
            "if (Valid?) then (Yes)\n"
            "  :Open Dashboard;\n"
            "  :Capture/Submit Data;\n"
            "  :Process Attendance;\n"
            "  :Generate Report;\n"
            "else (No)\n"
            "  :Show Error;\n"
            "endif\n"
            "stop\n"
            "@enduml"
        )

    if "use case" in safe_type:
        return (
            "@startuml\n"
            f"title Use Case Diagram - {safe_title}\n"
            "left to right direction\n"
            "actor Student\n"
            "actor Admin\n"
            "rectangle System {\n"
            "  usecase \"Login\" as UC1\n"
            "  usecase \"Submit Data\" as UC2\n"
            "  usecase \"Mark Attendance\" as UC3\n"
            "  usecase \"Generate Report\" as UC4\n"
            "}\n"
            "Student --> UC1\n"
            "Student --> UC4\n"
            "Admin --> UC1\n"
            "Admin --> UC2\n"
            "Admin --> UC3\n"
            "Admin --> UC4\n"
            "@enduml"
        )

    if "sequence" in safe_type:
        return (
            "@startuml\n"
            f"title Sequence Diagram - {safe_title}\n"
            "actor User\n"
            "participant UI\n"
            "participant API\n"
            "participant DB\n"
            "User -> UI: Submit data\n"
            "UI -> API: POST /attendance\n"
            "API -> DB: Save record\n"
            "DB --> API: OK\n"
            "API --> UI: Success response\n"
            "UI --> User: Show confirmation\n"
            "@enduml"
        )

    if "component" in safe_type:
        return (
            "@startuml\n"
            f"title Component Diagram - {safe_title}\n"
            "[Web UI] --> [Flask API]\n"
            "[Flask API] --> [AI Service]\n"
            "[Flask API] --> [Document Service]\n"
            "[Document Service] --> [DOCX Templates]\n"
            "[Flask API] --> [Database]\n"
            "@enduml"
        )

    if "deployment" in safe_type:
        return (
            "@startuml\n"
            f"title Deployment Diagram - {safe_title}\n"
            "node \"Client Browser\" {\n"
            "  component \"React Frontend\"\n"
            "}\n"
            "node \"Application Server\" {\n"
            "  component \"Flask Backend\"\n"
            "}\n"
            "node \"Storage\" {\n"
            "  database \"SQLite/DB\"\n"
            "  folder \"Uploads\"\n"
            "}\n"
            "\"React Frontend\" --> \"Flask Backend\"\n"
            "\"Flask Backend\" --> \"SQLite/DB\"\n"
            "\"Flask Backend\" --> \"Uploads\"\n"
            "@enduml"
        )

    if "database" in safe_type:
        return (
            "@startuml\n"
            f"title Database Model - {safe_title}\n"
            "entity USERS {\n"
            "  *id : int\n"
            "  name : string\n"
            "  role : string\n"
            "}\n"
            "entity PROJECTS {\n"
            "  *id : int\n"
            "  title : string\n"
            "  user_id : int\n"
            "}\n"
            "entity DIAGRAMS {\n"
            "  *id : int\n"
            "  project_id : int\n"
            "  type : string\n"
            "  filename : string\n"
            "}\n"
            "USERS ||--o{ PROJECTS\n"
            "PROJECTS ||--o{ DIAGRAMS\n"
            "@enduml"
        )

    return (
        "@startuml\n"
        f"title UML Diagram - {safe_title}\n"
        "actor User\n"
        "rectangle System {\n"
        "  usecase \"Login\" as UC1\n"
        "  usecase \"Generate Report\" as UC2\n"
        "}\n"
        "User --> UC1\n"
        "User --> UC2\n"
        "@enduml"
    )


def _generate_plantuml_via_hf(project_title: str, diagram_type: str, hf_api_key: str) -> str:
    """
    Call Hugging Face text model and return cleaned PlantUML.
    """
    prompt = _build_plantuml_prompt(project_title, diagram_type)
    model_url = f"{HF_ROUTER_BASE_URL}/{HF_PLANTUML_MODEL}"
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(
            model_url,
            headers=headers,
            json={"inputs": prompt, "options": {"wait_for_model": True}},
            timeout=120,
        )
        if not response.ok:
            message = f"Hugging Face request failed with status {response.status_code}"
            try:
                err = response.json()
                if isinstance(err, dict):
                    message = err.get("error") or err.get("message") or message
            except ValueError:
                if response.text:
                    message = response.text[:300]

            # If model is unavailable in router, use safe fallback PlantUML.
            if response.status_code == 404:
                return _fallback_plantuml(project_title, diagram_type)
            raise ValueError(message)

        payload = response.json()
        raw_text = _extract_text_from_hf_response(payload)
        candidate = _extract_plantuml_block(raw_text)
        if not _is_plantuml_suitable_for_type(candidate, diagram_type):
            return _fallback_plantuml(project_title, diagram_type)
        return candidate
    except Exception:
        return _fallback_plantuml(project_title, diagram_type)


def _render_plantuml_with_kroki(plantuml_code: str) -> bytes:
    """
    Send PlantUML text to Kroki and return PNG bytes.
    """
    response = requests.post(
        KROKI_PLANTUML_PNG_URL,
        headers={"Content-Type": "text/plain"},
        data=plantuml_code.encode("utf-8"),
        timeout=120,
    )
    if not response.ok:
        message = f"Kroki rendering failed with status {response.status_code}"
        if response.text:
            message = response.text[:300]
        raise ValueError(message)
    return response.content


def success_response(message, data=None, status=200):
    return jsonify({"success": True, "message": message, "data": data or {}}), status


def error_response(message, status=400, data=None):
    return jsonify({"success": False, "message": message, "data": data or {}}), status


@app.get("/uploads/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/api/templates")
def api_templates():
    try:
        templates = template_service.list_templates()
        return success_response("Templates loaded", {"templates": templates})
    except Exception as exc:
        return error_response("Failed to load templates", 500, {"error": str(exc)})


@app.post("/api/preview")
def api_preview():
    try:
        payload = request.get_json(force=True, silent=False)
        html = render_preview_html(payload)
        return success_response("Preview rendered", {"html": html})
    except Exception as exc:
        return error_response("Failed to render preview", 400, {"error": str(exc)})


@app.post("/api/generate-ai")
def api_generate_ai():
    try:
        data = request.get_json(force=True, silent=False)
        project_title = str(data.get("project_title", "")).strip()
        if not project_title:
            return error_response("project_title is required", 400)

        docs = ai_service.generate_documentation(project_title)
        return success_response("AI content generated", {"documentation": docs})
    except ValueError as exc:
        return error_response(str(exc), 400)
    except Exception as exc:
        return error_response("AI generation failed", 500, {"error": str(exc)})


@app.post("/api/upload-files")
def api_upload_files():
    try:
        code_saved = save_uploaded_list(request.files.getlist("codeFiles"), UPLOAD_DIR)
        screenshot_saved = save_uploaded_list(request.files.getlist("screenshots"), UPLOAD_DIR)
        diagram_saved = save_uploaded_list(request.files.getlist("diagrams"), UPLOAD_DIR)
        plagiarism_saved = save_uploaded_list(request.files.getlist("plagiarism_report"), UPLOAD_DIR)

        code_payload = []
        for item in code_saved:
            with open(item["path"], "r", encoding="utf-8", errors="ignore") as fh:
                code_payload.append(
                    {
                        "name": item["original_name"],
                        "filename": item["filename"],
                        "language": guess_language(item["original_name"]),
                        "content": fh.read(),
                    }
                )

        return success_response(
            "Files uploaded",
            {
                "codeFiles": code_payload,
                "screenshots": screenshot_saved,
                "diagrams": diagram_saved,
                "plagiarism_report": plagiarism_saved[0] if plagiarism_saved else None,
            },
        )
    except Exception as exc:
        return error_response("File upload failed", 500, {"error": str(exc)})


@app.route("/generate_diagrams", methods=["POST"])
def generate_diagrams():
    try:
        # Step 1: Read JSON body and validate required fields.
        payload = request.get_json(silent=True) or {}
        project_title = str(payload.get("project_title", "")).strip()
        diagram_type = str(payload.get("diagram_type", "")).strip()

        if not project_title:
            return jsonify({"status": "error", "error": "project_title is required"}), 400
        if not diagram_type:
            return jsonify({"status": "error", "error": "diagram_type is required"}), 400

        hf_api_key = os.getenv("HF_API_KEY", "").strip()
        if not hf_api_key:
            return jsonify({"status": "error", "error": "HF_API_KEY is missing"}), 500

        # Step 2: Generate PlantUML from Hugging Face text model.
        plantuml_code = _generate_plantuml_via_hf(project_title, diagram_type, hf_api_key)

        # Step 3: Render PlantUML to PNG using Kroki.
        image_bytes = _render_plantuml_with_kroki(plantuml_code)

        # Step 4: Save generated PNG in uploads folder.
        timestamp = int(time.time())
        diagram_slug = _safe_diagram_slug(diagram_type)
        filename = f"{diagram_slug}_{timestamp}.png"
        upload_folder = app.config.get("UPLOAD_FOLDER") or UPLOAD_DIR
        Path(upload_folder).mkdir(parents=True, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)

        with open(save_path, "wb") as image_file:
            image_file.write(image_bytes)

        # Step 5: Return saved filename to frontend.
        return jsonify({"status": "success", "filename": filename}), 200
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except requests.RequestException as exc:
        return jsonify({"status": "error", "error": f"External request failed: {exc}"}), 502
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500


@app.route("/generate_diagram_ai", methods=["POST"])
def generate_diagram_ai():
    # Backward-compatible alias.
    return generate_diagrams()


@app.post("/api/generate-document")
def api_generate_document():
    try:
        payload = extract_form_payload(request.form)

        selected_template = payload.get("selectedTemplate", "")
        if not selected_template:
            return error_response("Missing template", 400)

        template_info = template_service.get_template(selected_template)
        if not template_info:
            return error_response("Invalid template selected", 400)

        student_details = payload.get("studentDetails", {})
        missing_student = validate_student_details(student_details)
        if missing_student:
            return error_response("Missing required student fields", 400, {"missing": missing_student})

        documentation = payload.get("documentation", {})
        empty_docs = validate_documentation(documentation)
        if empty_docs:
            return error_response("Documentation sections cannot be empty", 400, {"empty_sections": empty_docs})

        template_path = os.path.join(BASE_DIR, template_info.get("file", ""))

        code_saved = save_uploaded_list(request.files.getlist("codeFiles"), UPLOAD_DIR)
        screenshot_saved = save_uploaded_list(request.files.getlist("screenshots"), UPLOAD_DIR)
        diagram_saved = save_uploaded_list(request.files.getlist("diagrams"), UPLOAD_DIR)
        plagiarism_saved = save_uploaded_list(request.files.getlist("plagiarism_report"), UPLOAD_DIR)

        code_items = []
        for item in code_saved:
            with open(item["path"], "r", encoding="utf-8", errors="ignore") as fh:
                code_items.append(
                    {
                        "name": item["original_name"],
                        "filename": item["original_name"],
                        "language": guess_language(item["original_name"]),
                        "content": fh.read(),
                    }
                )

        screenshots_meta = payload.get("screenshotsMeta", [])
        screenshots = []
        for idx, item in enumerate(screenshot_saved):
            name = (
                screenshots_meta[idx].get("name")
                if idx < len(screenshots_meta) and isinstance(screenshots_meta[idx], dict)
                else item["original_name"]
            )
            screenshots.append({"name": name or item["original_name"], "path": item["path"]})

        diagrams_meta = payload.get("diagramsMeta", [])
        diagrams = []
        for idx, item in enumerate(diagram_saved):
            name = diagrams_meta[idx].get("name") if idx < len(diagrams_meta) and isinstance(diagrams_meta[idx], dict) else item["original_name"]
            diagrams.append({"name": name or item["original_name"], "path": item["path"]})

        plagiarism_report = None
        if plagiarism_saved:
            plagiarism_report = {
                "title": payload.get("plagiarism_report_title") or "Plagiarism Report",
                "name": plagiarism_saved[0]["original_name"],
                "path": plagiarism_saved[0]["path"],
            }

        out_name, out_path = generate_document(
            template_path=template_path,
            template_config=template_info,
            payload=payload,
            code_items=code_items,
            screenshots=screenshots,
            diagrams=diagrams,
            plagiarism_report=plagiarism_report,
        )

        return success_response(
            "Document generated",
            {
                "file_name": out_name,
                "file_path": out_path,
                "download_url": f"/api/download/{out_name}",
            },
        )

    except FileNotFoundError as exc:
        return error_response(str(exc), 404)
    except Exception as exc:
        return error_response("Document generation failed", 500, {"error": str(exc)})


@app.get("/api/download/<filename>")
def api_download(filename):
    try:
        file_path = os.path.join(GENERATED_DIR, filename)
        if not os.path.exists(file_path):
            return error_response("File not found", 404)
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as exc:
        return error_response("Download failed", 500, {"error": str(exc)})


if __name__ == "__main__":
    # Keep debug traceback, but disable auto-reloader to avoid request interruption
    # when uploaded/generated files are written during active requests.
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
