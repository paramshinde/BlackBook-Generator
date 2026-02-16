import bleach

from .pagination import paginate_sections


def render_document_html(document: dict, template_settings: dict) -> str:
    title = bleach.clean(document.get("meta", {}).get("projectTitle", "Untitled Project"))
    sections = document.get("sections", [])

    content_parts = [f"<h1>{title}</h1>"]
    for section in sections:
        heading = bleach.clean(section.get("heading", ""))
        body = bleach.clean(section.get("content", "")).replace("\n", "<br />")
        content_parts.append(f"<section><h2>{heading}</h2><p>{body}</p></section>")

    pages = paginate_sections(sections)
    html = "".join(content_parts)
    return f'<div data-pages="{pages}">{html}</div>'
