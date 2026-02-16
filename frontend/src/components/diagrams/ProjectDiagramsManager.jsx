import React, { useMemo, useState } from "react";

const DIAGRAM_TYPES = [
  { key: "event_table", label: "A. Event Table" },
  { key: "entity_relationship", label: "B. Entity Relationship Diagram" },
  { key: "class", label: "C. Class Diagram" },
  { key: "activity", label: "D. Activity Diagram" },
  { key: "use_case", label: "E. Use Case Diagram" },
  { key: "sequence", label: "F. Sequence Diagram" },
  { key: "component", label: "G. Component Diagram" },
  { key: "deployment", label: "H. Deployment Diagram" },
  { key: "database", label: "I. Database Diagram" },
];

function spinner() {
  return <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-indigo-600 align-middle" />;
}

export default function ProjectDiagramsManager({ projectTitle, diagrams, setDiagrams }) {
  const [loadingKey, setLoadingKey] = useState("");
  const [messages, setMessages] = useState({});
  const [aiFilenames, setAiFilenames] = useState({});

  const diagramByKey = useMemo(() => {
    const mapped = {};
    (diagrams || []).forEach((item) => {
      if (item?.diagramKey) mapped[item.diagramKey] = item;
    });
    return mapped;
  }, [diagrams]);

  const updateDiagram = (diagramKey, updater) => {
    setDiagrams((prev) => {
      const list = Array.isArray(prev) ? [...prev] : [];
      const index = list.findIndex((item) => item.diagramKey === diagramKey);
      const previous = index >= 0 ? list[index] : null;
      const next = typeof updater === "function" ? updater(previous) : updater;
      if (!next) return list;
      if (index >= 0) list[index] = next;
      else list.push(next);
      return list;
    });
  };

  const setMessage = (diagramKey, type, text) => {
    setMessages((prev) => ({ ...prev, [diagramKey]: { type, text } }));
  };

  const handleManualUpload = (diagramKey, diagramLabel, event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setAiFilenames((prev) => ({ ...prev, [diagramKey]: "" }));
    setMessage(diagramKey, "success", "Manual upload selected. AI version overridden.");

    updateDiagram(diagramKey, {
      diagramKey,
      name: diagramLabel.replace(/^[A-I]\.\s+/, ""),
      file,
      source: "manual",
      previewUrl: URL.createObjectURL(file),
    });
  };

  const handleGenerate = async (diagramKey, diagramLabel) => {
    const title = (projectTitle || "").trim();
    if (!title) {
      setMessage(diagramKey, "error", "Enter Project Title first.");
      return;
    }

    setLoadingKey(diagramKey);
    setMessage(diagramKey, "info", "Generating diagram...");

    try {
      const response = await fetch("/generate_diagrams", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_title: title,
          diagram_type: diagramLabel.replace(/^[A-I]\.\s+/, ""),
        }),
      });

      const payload = await response.json();
      if (!response.ok || payload.status !== "success") {
        throw new Error(payload.error || "Diagram generation failed.");
      }

      const filename = payload.filename;
      const fileResponse = await fetch(`/uploads/${encodeURIComponent(filename)}`);
      if (!fileResponse.ok) {
        throw new Error("Generated image could not be fetched.");
      }
      const blob = await fileResponse.blob();
      const file = new File([blob], filename, { type: blob.type || "image/png" });

      setAiFilenames((prev) => ({ ...prev, [diagramKey]: filename }));
      updateDiagram(diagramKey, {
        diagramKey,
        name: diagramLabel.replace(/^[A-I]\.\s+/, ""),
        file,
        source: "ai",
        aiFilename: filename,
        previewUrl: `/uploads/${encodeURIComponent(filename)}?t=${Date.now()}`,
      });
      setMessage(diagramKey, "success", "Diagram generated successfully.");
    } catch (error) {
      setMessage(diagramKey, "error", error.message || "Diagram generation failed.");
    } finally {
      setLoadingKey("");
    }
  };

  return (
    <div className="space-y-3">
      <h3 className="text-base font-bold text-slate-900">📊 Project Diagrams Manager</h3>
      {DIAGRAM_TYPES.map((item) => {
        const data = diagramByKey[item.key];
        const msg = messages[item.key];
        const isLoading = loadingKey === item.key;
        const inputId = `diagram-upload-${item.key}`;
        const previewSrc = data?.previewUrl || "";

        return (
          <div key={item.key} className="rounded-xl border border-slate-200 bg-white p-3">
            <h4 className="mb-2 text-sm font-semibold text-slate-900">{item.label}</h4>
            <div className="grid gap-2 md:grid-cols-[1fr_220px]">
              <input
                id={inputId}
                type="file"
                accept="image/*"
                onChange={(e) => handleManualUpload(item.key, item.label, e)}
                className="rounded border border-slate-300 px-2 py-2 text-sm"
              />
              <button
                type="button"
                disabled={isLoading}
                onClick={() => handleGenerate(item.key, item.label)}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-semibold text-white disabled:opacity-60"
              >
                {isLoading ? spinner() : null}
                {isLoading ? "Generating..." : "Generate with AI"}
              </button>
            </div>

            <input type="hidden" value={aiFilenames[item.key] || ""} readOnly />

            {msg?.text ? (
              <p
                className={`mt-2 text-xs ${
                  msg.type === "error"
                    ? "text-red-600"
                    : msg.type === "success"
                      ? "text-emerald-600"
                      : "text-slate-600"
                }`}
              >
                {msg.text}
              </p>
            ) : null}

            {previewSrc ? (
              <img src={previewSrc} alt={`${item.label} preview`} className="mt-2 max-h-56 w-full rounded border border-slate-200 bg-slate-50 object-contain" />
            ) : null}
          </div>
        );
      })}
    </div>
  );
}
