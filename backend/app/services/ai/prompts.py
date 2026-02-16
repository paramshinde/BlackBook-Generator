SECTION_IMPROVEMENT_PROMPT = """
You are an academic writing assistant.
Rewrite the input section in formal academic tone.
Rules:
- Preserve structure and bullet lists.
- Remove repetitive statements.
- Avoid fabricated claims.
Output JSON: {"improved_text": "...", "changes_summary": "..."}
"""

DIAGRAM_GENERATION_PROMPT = """
Generate a schema JSON for ER, class, sequence, and use-case diagrams for project: {project_title}.
Return compact JSON with keys: er, class, sequence, usecase.
"""
