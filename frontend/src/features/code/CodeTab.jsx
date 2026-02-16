import React from "react";
import CodeUploader from "../../components/uploads/CodeUploader";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function CodeTab() {
  const files = useBlackbookStore((s) => s.codeFiles);

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Code Implementation</h2>
      <CodeUploader />
      <div className="space-y-2">
        {files.map((file) => (
          <div key={file.filename} className="rounded border bg-white p-3 text-sm">
            <div className="font-semibold">{file.filename}</div>
            <div className="text-xs text-slate-500">{file.language || "auto-detected"}</div>
            <pre className="mt-2 max-h-40 overflow-auto rounded bg-slate-100 p-2 text-xs">{file.content_text || ""}</pre>
          </div>
        ))}
      </div>
    </div>
  );
}
