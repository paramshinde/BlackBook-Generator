import React from "react";

export default function SuccessPanel({ fileName, downloadUrl, onDownload, onReset }) {
  return (
    <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6 text-center">
      <h3 className="text-xl font-bold text-emerald-700">Document Generated Successfully</h3>
      <p className="mt-2 text-sm text-emerald-700">{fileName}</p>
      <div className="mt-4 flex items-center justify-center gap-2">
        <button
          type="button"
          onClick={() => onDownload(downloadUrl, fileName)}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white"
        >
          Download Black Book
        </button>
        <button type="button" onClick={onReset} className="rounded-lg border border-emerald-400 px-4 py-2 text-sm text-emerald-700">
          Generate Another
        </button>
      </div>
    </div>
  );
}
