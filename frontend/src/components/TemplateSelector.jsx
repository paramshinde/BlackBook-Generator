import React from "react";

const fieldClass = "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm";

export default function TemplateSelector({ templates, selectedTemplate, onChange }) {
  return (
    <div className="space-y-2 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <label className="text-sm font-semibold text-slate-700">Template</label>
      <select className={fieldClass} value={selectedTemplate} onChange={(e) => onChange(e.target.value)}>
        <option value="">Select template</option>
        {templates.map((t) => (
          <option key={t.id} value={t.id}>
            {t.name}
          </option>
        ))}
      </select>
    </div>
  );
}
