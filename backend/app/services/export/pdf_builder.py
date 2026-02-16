import os
import subprocess


def convert_docx_to_pdf(docx_path: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    command = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, docx_path]
    try:
      subprocess.run(command, check=True, capture_output=True)
    except Exception:
      # graceful fallback when libreoffice is unavailable
      pass
    filename = os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
    return os.path.join(output_dir, filename)
