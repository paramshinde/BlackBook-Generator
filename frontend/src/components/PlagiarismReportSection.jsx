import React from "react";

export default function PlagiarismReportSection({ report, onTitleChange, onFileChange, onRemove }) {
  return (
    <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800">Plagiarism Report</h3>
      <label className="block space-y-1">
        <span className="text-xs font-semibold text-slate-600">Report Title (Optional)</span>
        <input
          value={report.title}
          onChange={(e) => onTitleChange(e.target.value)}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Turnitin Similarity Report"
        />
      </label>

      <label className="block rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm">
        Upload PDF/JPG/PNG
        <input
          type="file"
          accept=".pdf,image/png,image/jpeg"
          className="mt-2 w-full"
          onChange={(e) => onFileChange(e.target.files?.[0] || null)}
        />
      </label>

      {report.file ? (
        <div className="flex items-center justify-between rounded-lg bg-slate-100 px-3 py-2 text-xs">
          <span>{report.file.name}</span>
          <button type="button" className="text-red-600" onClick={onRemove}>
            Remove
          </button>
        </div>
      ) : null}
    </div>
  );
}
