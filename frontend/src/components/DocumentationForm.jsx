import React from "react";

const keys = [
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
];

const textareaClass = "min-h-28 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm";

export default function DocumentationForm({ documentation, onChange }) {
  const filled = keys.filter((key) => (documentation[key] || "").trim()).length;
  const pct = Math.round((filled / keys.length) * 100);

  return (
    <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-slate-800">Documentation</h3>
        <span className="text-xs text-slate-500">{pct}% complete</span>
      </div>
      {keys.map((key) => (
        <label key={key} className="block space-y-1">
          <span className="text-xs font-semibold text-slate-600">{key.replace("doc_", "").replaceAll("_", " ")}</span>
          <textarea
            className={textareaClass}
            value={documentation[key] || ""}
            onChange={(e) => onChange(key, e.target.value)}
          />
        </label>
      ))}
    </div>
  );
}
