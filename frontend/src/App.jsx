import React, { useEffect, useMemo, useState } from "react";
import ConfirmModal from "./components/ConfirmModal";
import DocumentationForm from "./components/DocumentationForm";
import FileUploadSection from "./components/FileUploadSection";
import LoadingOverlay from "./components/LoadingOverlay";
import Notification from "./components/Notification";
import PlagiarismReportSection from "./components/PlagiarismReportSection";
import PreviewPane from "./components/PreviewPane";
import ProgressHeader from "./components/ProgressHeader";
import ProjectDiagramsManager from "./components/diagrams/ProjectDiagramsManager";
import ReferencesSection from "./components/ReferencesSection";
import StudentDetailsForm from "./components/StudentDetailsForm";
import SuccessPanel from "./components/SuccessPanel";
import TabNavigation from "./components/TabNavigation";
import TemplateSelector from "./components/TemplateSelector";
import { downloadFile, fetchTemplates, generateDocument, requestAIContent, requestPreview } from "./services/api";

const defaultDocumentation = {
  doc_introduction: "",
  doc_objective: "",
  doc_scope: "",
  doc_techstack: "",
  doc_feasibility: "",
  doc_system_features: "",
  doc_modules: "",
  doc_usecase: "",
  doc_advantage: "",
  doc_hardware_req: "",
  doc_software_req: "",
};

const defaultState = {
  selectedTemplate: "",
  studentDetails: {
    name: "",
    project: "",
    professor: "",
    guide: "",
    year: "",
  },
  documentation: defaultDocumentation,
  codeFiles: [],
  screenshots: [],
  diagrams: [],
  references: [{ label: "", url: "" }],
  plagiarismReport: {
    title: "",
    file: null,
  },
};

const DRAFT_KEY = "blackbook-draft-v2";

function uid() {
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export default function App() {
  const [state, setState] = useState(defaultState);
  const [templates, setTemplates] = useState([]);
  const [previewHtml, setPreviewHtml] = useState("<p>Preview will appear here.</p>");
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [loadingAI, setLoadingAI] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("details");
  const [toasts, setToasts] = useState([]);
  const [result, setResult] = useState(null);

  const pushToast = (type, message) => {
    const id = uid();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3500);
  };

  useEffect(() => {
    let mounted = true;
    const draftRaw = localStorage.getItem(DRAFT_KEY);

    if (draftRaw) {
      try {
        const draft = JSON.parse(draftRaw);
        setState((prev) => ({
          ...prev,
          ...draft,
          documentation: { ...defaultDocumentation, ...(draft.documentation || {}) },
          references: Array.isArray(draft.references) && draft.references.length ? draft.references : prev.references,
        }));
      } catch {
        localStorage.removeItem(DRAFT_KEY);
      }
    }

    (async () => {
      try {
        const list = await fetchTemplates();
        if (!mounted) return;
        setTemplates(list);
        setState((prev) => ({ ...prev, selectedTemplate: prev.selectedTemplate || list[0]?.id || "" }));
      } catch {
        if (!mounted) return;
        pushToast("error", "Failed to fetch templates.");
      }
    })();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    const serializable = {
      ...state,
      codeFiles: state.codeFiles.map((f) => ({ name: f.name, size: f.size })),
      screenshots: state.screenshots.map((item) => {
        const file = item?.file || item;
        return {
          name: item?.name || file?.name || "",
          fileName: file?.name || "",
          size: file?.size || 0,
        };
      }),
      diagrams: state.diagrams.map((d) => ({ name: d.name, fileName: d.file?.name || "" })),
      references: state.references,
      plagiarismReport: {
        title: state.plagiarismReport.title,
        fileName: state.plagiarismReport.file?.name || "",
      },
    };
    localStorage.setItem(DRAFT_KEY, JSON.stringify(serializable));
  }, [state]);

  const previewPayload = useMemo(
    () => ({
      selectedTemplate: state.selectedTemplate,
      studentDetails: state.studentDetails,
      documentation: state.documentation,
    }),
    [state.selectedTemplate, state.studentDetails, state.documentation]
  );

  useEffect(() => {
    const timeout = setTimeout(async () => {
      try {
        setLoadingPreview(true);
        const res = await requestPreview(previewPayload);
        setPreviewHtml(res.html || "<p>No preview content.</p>");
      } catch {
        pushToast("error", "Preview generation failed.");
      } finally {
        setLoadingPreview(false);
      }
    }, 350);

    return () => clearTimeout(timeout);
  }, [previewPayload]);

  const completion = useMemo(() => {
    const requiredStudent = ["name", "project", "professor", "guide", "year"];
    const studentDone = requiredStudent.filter((key) => (state.studentDetails[key] || "").trim()).length;
    const docKeys = Object.keys(defaultDocumentation);
    const docsDone = docKeys.filter((key) => (state.documentation[key] || "").trim()).length;

    const total = 1 + requiredStudent.length + docKeys.length + 3;
    const referencesDone = (state.references || []).some((ref) => (ref?.url || "").trim()) ? 1 : 0;
    const done =
      (state.selectedTemplate ? 1 : 0) +
      studentDone +
      docsDone +
      (state.codeFiles.length ? 1 : 0) +
      (state.screenshots.length ? 1 : 0) +
      (state.diagrams.length ? 1 : 0) +
      referencesDone;

    return Math.round((done / (total + 1)) * 100);
  }, [state]);

  const completionByTab = useMemo(() => {
    const docKeys = Object.keys(defaultDocumentation);
    const docDone = docKeys.filter((key) => (state.documentation[key] || "").trim()).length;

    return {
      details: Math.round(
        ([state.selectedTemplate, ...Object.values(state.studentDetails)].filter((x) => `${x}`.trim()).length / 6) * 100
      ),
      documentation: Math.round((docDone / docKeys.length) * 100),
      code: state.codeFiles.length > 0 ? 100 : 0,
      screenshots: state.screenshots.length > 0 ? 100 : 0,
      diagrams: state.diagrams.length > 0 ? 100 : 0,
      references: (state.references || []).some((ref) => (ref?.url || "").trim()) ? 100 : 0,
      preview: previewHtml.includes("<p>") ? 100 : 0,
      export: result ? 100 : 0,
    };
  }, [state, previewHtml, result]);

  const isReadyToGenerate =
    state.selectedTemplate &&
    ["name", "project", "professor", "guide", "year"].every((k) => (state.studentDetails[k] || "").trim()) &&
    Object.values(state.documentation).some((value) => (value || "").trim());

  const setStudentField = (key, value) => {
    setState((prev) => ({
      ...prev,
      studentDetails: { ...prev.studentDetails, [key]: value },
    }));
  };

  const setDocField = (key, value) => {
    setState((prev) => ({
      ...prev,
      documentation: { ...prev.documentation, [key]: value },
    }));
  };

  const handleAIGenerate = async () => {
    const projectTitle = (state.studentDetails.project || "").trim();
    if (!projectTitle) {
      pushToast("error", "Enter project title before AI generation.");
      return;
    }

    try {
      setLoadingAI(true);
      const aiDocs = await requestAIContent(projectTitle);
      setState((prev) => ({ ...prev, documentation: { ...prev.documentation, ...aiDocs } }));
      pushToast("success", "AI content generated successfully.");
    } catch (error) {
      pushToast("error", error.message || "AI generation failed.");
    } finally {
      setLoadingAI(false);
    }
  };

  const handleSubmit = async () => {
    if (!isReadyToGenerate) {
      pushToast("error", "Complete required fields before generating.");
      return;
    }

    try {
      setSubmitting(true);
      setResult(null);
      const formData = new FormData();
      formData.append("selectedTemplate", state.selectedTemplate);
      formData.append("studentDetails", JSON.stringify(state.studentDetails));
      formData.append("documentation", JSON.stringify(state.documentation));
      formData.append(
        "diagramsMeta",
        JSON.stringify(state.diagrams.map((item) => ({ name: item.name || item.file?.name || "Diagram" })))
      );
      formData.append(
        "screenshotsMeta",
        JSON.stringify(
          state.screenshots.map((item) => {
            const file = item?.file || item;
            return { name: (item?.name || file?.name || "Screenshot").trim() };
          })
        )
      );
      formData.append(
        "references",
        JSON.stringify(
          (state.references || [])
            .map((ref) => ({
              label: (ref?.label || "").trim(),
              url: (ref?.url || "").trim(),
            }))
            .filter((ref) => ref.url)
        )
      );
      formData.append("codeFilesMeta", JSON.stringify(state.codeFiles.map((file) => ({ name: file.name }))));

      state.codeFiles.forEach((file) => formData.append("codeFiles", file));
      state.screenshots.forEach((item) => {
        const file = item?.file || item;
        if (file && typeof file === "object" && typeof file.arrayBuffer === "function") {
          formData.append("screenshots", file);
        }
      });
      state.diagrams.forEach((item) => {
        if (item.file) formData.append("diagrams", item.file);
      });

      if (state.plagiarismReport.file) {
        formData.append("plagiarism_report", state.plagiarismReport.file);
      }
      formData.append("plagiarism_report_title", state.plagiarismReport.title || "Plagiarism Report");

      const res = await generateDocument(formData);
      setResult(res);
      setActiveTab("export");
      pushToast("success", "Black Book generated successfully.");
    } catch (error) {
      pushToast("error", error.message || "Document generation failed.");
    } finally {
      setSubmitting(false);
      setConfirmOpen(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.download_url) {
      pushToast("error", "Download URL missing.");
      return;
    }
    try {
      await downloadFile(result.download_url, result.file_name || "blackbook.docx");
    } catch (error) {
      pushToast("error", error.message || "Download failed.");
    }
  };

  const renderTab = () => {
    if (activeTab === "details") {
      return (
        <div className="space-y-4">
          <TemplateSelector
            templates={templates}
            selectedTemplate={state.selectedTemplate}
            onChange={(value) => setState((prev) => ({ ...prev, selectedTemplate: value }))}
          />
          <StudentDetailsForm details={state.studentDetails} onChange={setStudentField} />
        </div>
      );
    }

    if (activeTab === "documentation") {
      return (
        <div className="space-y-4">
          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <button
              type="button"
              onClick={handleAIGenerate}
              disabled={loadingAI}
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
            >
              {loadingAI ? <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white" /> : null}
              {loadingAI ? "Generating..." : "Generate AI Content"}
            </button>
          </div>
          <DocumentationForm documentation={state.documentation} onChange={setDocField} />
        </div>
      );
    }

    if (activeTab === "code") {
      return (
        <FileUploadSection
          codeFiles={state.codeFiles}
          screenshots={undefined}
          diagrams={undefined}
          setCodeFiles={(value) => setState((prev) => ({ ...prev, codeFiles: value }))}
          setScreenshots={undefined}
          setDiagrams={undefined}
        />
      );
    }

    if (activeTab === "screenshots") {
      return (
        <FileUploadSection
          codeFiles={undefined}
          screenshots={state.screenshots}
          diagrams={undefined}
          setCodeFiles={undefined}
          setScreenshots={(value) => setState((prev) => ({ ...prev, screenshots: value }))}
          setDiagrams={undefined}
        />
      );
    }

    if (activeTab === "diagrams") {
      return (
        <div className="space-y-4">
          <ProjectDiagramsManager
            projectTitle={state.studentDetails.project}
            diagrams={state.diagrams}
            setDiagrams={(valueOrUpdater) =>
              setState((prev) => ({
                ...prev,
                diagrams:
                  typeof valueOrUpdater === "function"
                    ? valueOrUpdater(prev.diagrams)
                    : valueOrUpdater,
              }))
            }
          />
          <PlagiarismReportSection
            report={state.plagiarismReport}
            onTitleChange={(title) =>
              setState((prev) => ({ ...prev, plagiarismReport: { ...prev.plagiarismReport, title } }))
            }
            onFileChange={(file) =>
              setState((prev) => ({ ...prev, plagiarismReport: { ...prev.plagiarismReport, file } }))
            }
            onRemove={() =>
              setState((prev) => ({ ...prev, plagiarismReport: { ...prev.plagiarismReport, file: null } }))
            }
          />
        </div>
      );
    }

    if (activeTab === "preview") {
      return <PreviewPane html={previewHtml} loading={loadingPreview} />;
    }

    if (activeTab === "references") {
      return (
        <ReferencesSection
          references={state.references}
          onChange={(references) => setState((prev) => ({ ...prev, references }))}
        />
      );
    }

    return (
      <div className="space-y-4">
        {result ? (
          <SuccessPanel
            fileName={result.file_name}
            downloadUrl={result.download_url}
            onDownload={handleDownload}
            onReset={() => setResult(null)}
          />
        ) : (
          <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <h3 className="text-lg font-bold text-slate-800">Export</h3>
            <p className="mt-2 text-sm text-slate-600">Generate your formatted black book document.</p>
            <button
              type="button"
              disabled={!isReadyToGenerate}
              onClick={() => setConfirmOpen(true)}
              className="mt-4 rounded-lg bg-emerald-600 px-5 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              Generate DOCX
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <ProgressHeader completion={completion} />
      <Notification toasts={toasts} onDismiss={(id) => setToasts((prev) => prev.filter((t) => t.id !== id))} />

      <main className="mx-auto max-w-7xl space-y-4 p-4">
        <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} completionByTab={completionByTab} />
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition-all duration-300">{renderTab()}</div>
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm">
            <h3 className="mb-3 text-sm font-bold text-slate-700">Live Preview</h3>
            <PreviewPane html={previewHtml} loading={loadingPreview} />
          </div>
        </div>
      </main>

      <ConfirmModal
        open={confirmOpen}
        title="Generate Final Black Book"
        description="This will build the DOCX using your latest details, documentation, code, screenshots, diagrams, references, and plagiarism report."
        onCancel={() => setConfirmOpen(false)}
        onConfirm={handleSubmit}
      />

      <LoadingOverlay show={submitting} label="Generating Black Book document..." />
    </div>
  );
}
