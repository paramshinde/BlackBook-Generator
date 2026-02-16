import os

from flask import Blueprint, current_app, jsonify, request

from ..extensions import db
from ..models.code_file import ProjectCodeFile
from ..models.project import Project
from ..models.screenshot import ProjectScreenshot
from ..utils.storage import save_local_file, to_public_path
from ..utils.validators import validate_code_file, validate_image_file

bp = Blueprint("uploads", __name__, url_prefix="/api/projects")


def _detect_language(filename: str) -> str:
    ext = os.path.splitext(filename.lower())[1]
    return {
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
    }.get(ext, "text")


@bp.post("/<int:project_id>/uploads/screenshots")
def upload_screenshots(project_id: int):
    project = Project.query.get_or_404(project_id)
    files = request.files.getlist("files")
    items = []

    for index, file in enumerate(files, start=1):
        if not file or not validate_image_file(file.filename):
            continue
        path = save_local_file(current_app.config["UPLOAD_DIR"], file, prefix="screenshot")
        caption = os.path.splitext(file.filename)[0].replace("_", " ")
        figure_no = f"Figure {len(project.screenshots) + index}.1"
        shot = ProjectScreenshot(
            project_id=project.id,
            file_url=to_public_path(path),
            caption=caption,
            figure_no=figure_no,
            display_order=len(project.screenshots) + index,
        )
        db.session.add(shot)
        items.append({"fileUrl": to_public_path(path), "caption": caption, "figureNo": figure_no})

    db.session.commit()
    return jsonify({"items": items})


@bp.post("/<int:project_id>/uploads/code")
def upload_code(project_id: int):
    project = Project.query.get_or_404(project_id)
    files = request.files.getlist("files")
    items = []

    for file in files:
        if not file or not validate_code_file(file.filename):
            continue

        raw = file.read().decode("utf-8", errors="ignore")
        filename = file.filename
        language = _detect_language(filename)

        model = ProjectCodeFile(
            project_id=project.id,
            filename=filename,
            language=language,
            content_text=raw,
            line_count=len(raw.splitlines()),
        )
        db.session.add(model)
        items.append(
            {
                "filename": filename,
                "language": language,
                "content_text": raw,
                "line_count": len(raw.splitlines()),
            }
        )

    db.session.commit()
    return jsonify({"items": items})
