import React from "react";
import { useBlackbookStore } from "../../store/useBlackbookStore";

function Input({ label, value, onChange }) {
  return (
    <label className="grid gap-1 text-sm">
      <span className="font-semibold text-slate-700">{label}</span>
      <input className="rounded border border-slate-300 p-2" value={value || ""} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

export default function ProjectDetailsTab() {
  const projectDetails = useBlackbookStore((s) => s.projectDetails);
  const setProjectDetail = useBlackbookStore((s) => s.setProjectDetail);
  const setTemplate = useBlackbookStore((s) => s.setTemplate);
  const setDarkPreview = useBlackbookStore((s) => s.setDarkPreview);
  const templateSettings = useBlackbookStore((s) => s.templateSettings);

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Project Details</h2>
      <Input label="Project Title" value={projectDetails.projectTitle} onChange={(v) => setProjectDetail("projectTitle", v)} />
      <Input label="Student Name" value={projectDetails.studentName} onChange={(v) => setProjectDetail("studentName", v)} />
      <Input label="Guide Name" value={projectDetails.guideName} onChange={(v) => setProjectDetail("guideName", v)} />
      <Input label="Professor Name" value={projectDetails.professorName} onChange={(v) => setProjectDetail("professorName", v)} />
      <Input label="Tech Stack" value={projectDetails.techStack} onChange={(v) => setProjectDetail("techStack", v)} />
      <div className="rounded-lg border bg-white p-4">
        <h3 className="mb-2 text-sm font-bold">Template Settings</h3>
        <div className="flex flex-wrap gap-2">
          <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => setTemplate("ieee")}>IEEE</button>
          <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => setTemplate("college")}>College</button>
          <label className="rounded border px-3 py-2">
            <span className="mr-2 text-xs">Custom</span>
            <input type="file" className="text-xs" />
          </label>
        </div>
        <label className="mt-3 flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={templateSettings.darkPreview}
            onChange={(e) => setDarkPreview(e.target.checked)}
          />
          Dark preview mode
        </label>
      </div>
    </div>
  );
}
