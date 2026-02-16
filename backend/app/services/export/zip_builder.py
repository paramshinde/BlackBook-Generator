import json
import os
import zipfile


def build_zip(bundle_dir: str, output_path: str, metadata: dict) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    meta_path = os.path.join(bundle_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(bundle_dir):
            for file_name in files:
                full = os.path.join(root, file_name)
                rel = os.path.relpath(full, bundle_dir)
                zipf.write(full, rel)
    return output_path
