import os
import importlib.util
from pathlib import Path

from flask import Flask, jsonify

from .config import Config
from .extensions import cors, db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Models import for migration discovery
    from .models import (  # noqa: F401
        ai_job,
        code_file,
        diagram,
        export_job,
        plagiarism_report,
        project,
        screenshot,
        section,
        template,
        user,
        version,
    )

    from .api.routes_ai import bp as ai_bp
    from .api.routes_diagrams import bp as diagrams_bp
    from .api.routes_exports import bp as exports_bp
    from .api.routes_jobs import bp as jobs_bp
    from .api.routes_plagiarism import bp as plagiarism_bp
    from .api.routes_preview import bp as preview_bp
    from .api.routes_projects import bp as projects_bp
    from .api.routes_templates import bp as templates_bp
    from .api.routes_uploads import bp as uploads_bp
    from .api.routes_versions import bp as versions_bp
    from .api.routes_auth import bp as auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(preview_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(diagrams_bp)
    app.register_blueprint(plagiarism_bp)
    app.register_blueprint(exports_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(templates_bp)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    return app


def _load_legacy_app():
    """
    Prefer the legacy Flask app in backend/app.py so existing frontend routes
    (/api/*, /generate_diagrams, /uploads/*) continue to work.
    """
    app_py = Path(__file__).resolve().parent.parent / "app.py"
    spec = importlib.util.spec_from_file_location("legacy_app_module", app_py)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Flask app from {app_py}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


# Compatibility for process managers configured as "gunicorn app:app".
app = _load_legacy_app()
