import React from "react";

function emptyReference() {
  return { label: "", url: "" };
}

export default function ReferencesSection({ references, onChange }) {
  const list = Array.isArray(references) && references.length ? references : [emptyReference()];

  const updateItem = (index, key, value) => {
    const next = list.map((item, idx) => (idx === index ? { ...item, [key]: value } : item));
    onChange(next);
  };

  const addRow = () => {
    onChange([...list, emptyReference()]);
  };

  const removeRow = (index) => {
    const next = list.filter((_, idx) => idx !== index);
    onChange(next.length ? next : [emptyReference()]);
  };

  return (
    <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-base font-bold text-slate-900">References</h3>
      <p className="text-xs text-slate-600">Add websites you referred to. These links will be added in the final References section.</p>

      {list.map((item, index) => (
        <div key={`reference-${index}`} className="rounded-lg border border-slate-200 bg-slate-50 p-3">
          <div className="grid gap-2 md:grid-cols-[1fr_2fr_auto]">
            <input
              type="text"
              value={item.label || ""}
              onChange={(e) => updateItem(index, "label", e.target.value)}
              placeholder="Website name (optional)"
              className="rounded border border-slate-300 px-2 py-2 text-sm"
            />
            <input
              type="url"
              value={item.url || ""}
              onChange={(e) => updateItem(index, "url", e.target.value)}
              placeholder="https://example.com"
              className="rounded border border-slate-300 px-2 py-2 text-sm"
            />
            <button
              type="button"
              onClick={() => removeRow(index)}
              className="rounded border border-red-200 px-3 py-2 text-sm font-semibold text-red-600"
            >
              Remove
            </button>
          </div>
        </div>
      ))}

      <button
        type="button"
        onClick={addRow}
        className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700"
      >
        Add Website
      </button>
    </div>
  );
}
