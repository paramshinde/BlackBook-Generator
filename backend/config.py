import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_JSON_PATH = os.path.join(BASE_DIR, "templates.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_IMAGE_WIDTH_INCHES = 6.2
MAX_IMAGE_HEIGHT_INCHES = 8.0
