import mimetypes

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}
ALLOWED_CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".php", ".html", ".css", ".sql", ".json"}


def guess_mime(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def validate_image_file(filename: str) -> bool:
    return guess_mime(filename) in ALLOWED_IMAGE_TYPES


def validate_code_file(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in ALLOWED_CODE_EXTENSIONS)
