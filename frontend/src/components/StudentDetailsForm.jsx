import React from "react";

const inputClass = "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm";

function Row({ label, value, onChange, required }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm font-semibold text-slate-700">
        {label}
        {required ? <span className="text-red-500"> *</span> : null}
      </span>
      <input className={inputClass} value={value} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

export default function StudentDetailsForm({ details, onChange }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-bold text-slate-800">Student Details</h3>
      <div className="grid gap-3 sm:grid-cols-2">
        <Row label="Student Name" value={details.name} required onChange={(v) => onChange("name", v)} />
        <Row label="Project Title" value={details.project} required onChange={(v) => onChange("project", v)} />
        <Row label="Professor Name" value={details.professor} required onChange={(v) => onChange("professor", v)} />
        <Row label="Guide Name" value={details.guide} required onChange={(v) => onChange("guide", v)} />
        <Row label="Year" value={details.year} required onChange={(v) => onChange("year", v)} />
      </div>
    </div>
  );
}
