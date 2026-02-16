from html import escape

DOC_KEYS = [
    "doc_introduction",
    "doc_objective",
    "doc_scope",
    "doc_techstack",
    "doc_feasibility",
    "doc_system_features",
    "doc_modules",
    "doc_usecase",
    "doc_advantage",
    "doc_hardware_req",
    "doc_software_req",
]


def _cover_page_html(details: dict) -> str:
    project_title = escape(details.get("project", "Project Title"))
    student_name = escape(details.get("name", "Student Name"))
    guide_name = escape(details.get("guide", "Guide Name"))
    professor_name = escape(details.get("professor", "Professor Name"))
    year = escape(details.get("year", ""))
    seat_no = escape(details.get("seat_no", ""))

    return f"""
<style>
  .bb-preview {{
    font-family: "Times New Roman", Times, serif;
    color: #111;
  }}
  .bb-cover-page {{
    border: 1.5px solid #333;
    padding: 28px 42px;
    min-height: 980px;
    text-align: center;
    line-height: 1.25;
    background: #fff;
  }}
  .bb-cover-small {{ font-size: 22px; margin: 2px 0; }}
  .bb-cover-ital {{ font-size: 34px; font-style: italic; margin: 8px 0; }}
  .bb-cover-title {{
    font-size: 44px;
    font-weight: 700;
    text-decoration: underline;
    margin: 8px 0 16px;
  }}
  .bb-cover-name {{ font-size: 40px; font-weight: 700; margin: 8px 0; }}
  .bb-cover-main {{ font-size: 38px; font-weight: 700; margin: 8px 0; }}
  .bb-cover-mid {{ font-size: 34px; margin: 6px 0; }}
  .bb-cover-dept {{ font-size: 30px; font-weight: 700; margin: 8px 0 16px; }}
  .bb-cover-logo {{
    width: 150px;
    height: 150px;
    border: 2px solid #444;
    border-radius: 9999px;
    margin: 12px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 700;
  }}
  .bb-cover-college {{ font-size: 26px; font-weight: 700; margin-top: 8px; }}
  .bb-cover-sub {{ font-size: 20px; margin-top: 10px; }}
  .bb-doc-sections {{ margin-top: 30px; }}
  .bb-doc-sections h2 {{ font-size: 30px; margin: 20px 0 8px; }}
  .bb-doc-sections p {{ font-size: 20px; margin: 0; line-height: 1.55; }}
</style>
<div class="bb-preview">
  <section class="bb-cover-page">
    <p class="bb-cover-small">A Project Report</p>
    <p class="bb-cover-small">On</p>
    <p class="bb-cover-title">"{project_title}"</p>
    <p class="bb-cover-ital">Submitted by</p>
    <p class="bb-cover-name">{student_name}</p>
    <p class="bb-cover-mid"><strong>Seat no.:</strong> {seat_no}</p>
    <p class="bb-cover-ital">in partial fulfillment for the award of the degree of</p>
    <p class="bb-cover-main">BACHELOR OF SCIENCE</p>
    <p class="bb-cover-mid">in</p>
    <p class="bb-cover-main">COMPUTER SCIENCE</p>
    <p class="bb-cover-ital">under the guidance of</p>
    <p class="bb-cover-name">{guide_name}</p>
    <p class="bb-cover-dept">Department of Computer Science</p>
    <div class="bb-cover-logo">LOGO</div>
    <p class="bb-cover-college">VIDYAVARDHINI'S</p>
    <p class="bb-cover-dept">A.V. COLLEGE OF ARTS, K.M. COLLEGE OF COMMERCE, E.S.A. COLLEGE OF SCIENCE, VASAI (WEST)</p>
    <p class="bb-cover-mid">PALGHAR - 401202</p>
    <p class="bb-cover-sub">Affiliated To University Of Mumbai</p>
    <p class="bb-cover-mid">MAHARASHTRA</p>
    <p class="bb-cover-mid">(SEM-V)</p>
    <p class="bb-cover-mid">({year})</p>
    <p class="bb-cover-sub"><strong>Professor:</strong> {professor_name}</p>
  </section>
"""


def render_preview_html(payload: dict) -> str:
    details = payload.get("studentDetails", {})
    docs = payload.get("documentation", {})

    sections = [_cover_page_html(details), '<section class="bb-doc-sections">']

    for key in DOC_KEYS:
        label = key.replace("doc_", "").replace("_", " ").title()
        value = escape(docs.get(key, "")).replace("\n", "<br />")
        sections.append(f"<h2>{label}</h2><p>{value}</p>")

    sections.append("</section></div>")
    return "\n".join(sections)
