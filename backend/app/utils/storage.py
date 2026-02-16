import os
import re
import uuid
from pathlib import Path


def save_local_file(upload_dir: str, file_storage, prefix: str = "") -> str:
    ext = Path(file_storage.filename).suffix
    safe_prefix = re.sub(r"[^a-zA-Z0-9_-]", "", prefix)[:24]
    filename = f"{safe_prefix}_{uuid.uuid4().hex}{ext}" if safe_prefix else f"{uuid.uuid4().hex}{ext}"
    destination = os.path.join(upload_dir, filename)
    file_storage.save(destination)
    return destination


def to_public_path(abs_path: str) -> str:
    return abs_path.replace("\\", "/")
