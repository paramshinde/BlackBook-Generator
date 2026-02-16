import axios from "axios";

const api = axios.create({ baseURL: "/" });

function pickSectionContent(document, sectionId, fallback = "") {
  const section = (document?.sections || []).find((s) => s.id === sectionId);
  return section?.content || fallback;
}

function toPreviewPayload(payload = {}) {
  const document = payload.document || {};
  const meta = document.meta || {};

  return {
    template_file: "proj.docx",
    student_name: meta.studentName || "Student",
    project_title: meta.projectTitle || "Untitled Project",
    professor_name: meta.professorName || "Professor",
    guide_name: meta.guideName || "Guide",
    year: meta.year || "2025-2026",
    doc_introduction: pickSectionContent(document, "introduction"),
    doc_objective: pickSectionContent(document, "objective"),
    doc_scope: pickSectionContent(document, "scope"),
    doc_techstack: pickSectionContent(document, "techStack"),
    doc_modules: pickSectionContent(document, "modules"),
  };
}

function computePlagiarism(document = {}) {
  const sections = document.sections || [];
  const text = sections.map((s) => s.content || "").join(" ").toLowerCase();
  const words = text.split(/\s+/).filter(Boolean);
  const counts = new Map();
  for (const w of words) {
    if (w.length < 4) continue;
    counts.set(w, (counts.get(w) || 0) + 1);
  }
  const repeated = [...counts.entries()].filter(([, c]) => c > 8).length;
  const originality = Math.max(40, Math.min(100, 100 - repeated * 2));

  return {
    originality_percentage: originality,
    flagged_sections: sections
      .filter((s) => (s.content || "").length > 180 && (s.content || "").split(/\s+/).length < 35)
      .map((s) => ({ section_id: s.id, reason: "Low lexical diversity" })),
  };
}

export const apiClient = {
  async createProject() {
    return { data: { id: "local" } };
  },

  async getProject(id) {
    return { data: { id, title: "Local Project" } };
  },

  async autosave(_id, _payload) {
    return { data: { status: "saved" } };
  },

  renderPreview: (_id, payload) => api.post("/preview", toPreviewPayload(payload)),

  async improveSection(_id, sectionKey, payload) {
    const projectTitle = sectionKey || "Project Section";
    try {
      const { data } = await api.post("/generate_project_content", { project_title: projectTitle });
      const candidate =
        data.doc_introduction ||
        data.doc_objective ||
        data.doc_scope ||
        data.doc_techstack ||
        payload?.content ||
        "";
      return { data: { improved_text: candidate, changes_summary: "Generated from AI service." } };
    } catch {
      return {
        data: {
          improved_text: payload?.content || "",
          changes_summary: "AI service unavailable. Returned original content.",
        },
      };
    }
  },

  generateDiagrams: (_id, payload) => api.post("/generate_diagrams", payload),

  async plagiarismCheck(_id, payload) {
    return { data: computePlagiarism(payload?.document || {}) };
  },

  async uploadCode(_id, formData) {
    const files = formData.getAll("files");
    const items = await Promise.all(
      files.map(async (file) => {
        const content = await file.text();
        return {
          filename: file.name,
          language: "text",
          content_text: content,
          line_count: content.split("\n").length,
        };
      })
    );
    return { data: { items } };
  },

  async uploadScreenshots(_id, formData) {
    const files = formData.getAll("files");
    const items = files.map((file, idx) => ({
      fileUrl: "",
      previewUrl: URL.createObjectURL(file),
      caption: file.name,
      figureNo: `Figure ${idx + 1}.1`,
    }));
    return { data: { items } };
  },

  async exportDocx() {
    return { data: { job_id: "docx-ready" } };
  },

  async exportPdf() {
    return { data: { job_id: "pdf-ready" } };
  },

  async exportZip() {
    return { data: { job_id: "zip-ready" } };
  },

  async getJob(jobId) {
    return { data: { id: jobId, status: "completed" } };
  },
};
