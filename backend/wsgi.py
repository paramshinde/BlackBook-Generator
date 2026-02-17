"""
Render/Gunicorn entrypoint for the Flask app defined in app.py.

This avoids import ambiguity with the backend/app package.
"""

import importlib.util
from pathlib import Path


def _load_app():
    app_py = Path(__file__).with_name("app.py")
    spec = importlib.util.spec_from_file_location("legacy_app_module", app_py)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Flask app from {app_py}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


app = _load_app()
