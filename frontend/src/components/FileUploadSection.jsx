import React from "react";
import DropzoneField from "./DropzoneField";

function FileList({ title, files, onRemove, showNameInput, onNameChange }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h4 className="mb-2 text-sm font-bold text-slate-800">{title}</h4>
      {files.length === 0 ? <p className="text-xs text-slate-500">No files added.</p> : null}
      <div className="space-y-2">
        {files.map((item, index) => {
          const file = item.file || item;
          return (
            <div key={`${file.name}-${index}`} className="rounded-lg border border-slate-200 bg-slate-50 p-2">
              {showNameInput ? (
                <input
                  value={item.name}
                  onChange={(e) => onNameChange(index, e.target.value)}
                  placeholder={title === "Screenshots" ? "Screenshot Name" : "Diagram Name"}
                  className="mb-2 w-full rounded border border-slate-300 px-2 py-1 text-xs"
                />
              ) : null}
              <div className="flex items-center justify-between gap-2">
                <span className="truncate text-xs text-slate-700">{file.name}</span>
                <button type="button" className="text-xs font-semibold text-red-600" onClick={() => onRemove(index)}>
                  Remove
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function FileUploadSection({ codeFiles, screenshots, diagrams, setCodeFiles, setScreenshots, setDiagrams }) {
  const showCode = typeof setCodeFiles === "function";
  const showScreenshots = typeof setScreenshots === "function";
  const showDiagrams = typeof setDiagrams === "function";

  return (
    <div className="space-y-4">
      <div className="grid gap-3 md:grid-cols-3">
        {showCode ? (
          <DropzoneField
            title="Code Files"
            helper="Upload source files"
            onFiles={(files) => setCodeFiles([...(codeFiles || []), ...files])}
          />
        ) : null}
        {showScreenshots ? (
          <DropzoneField
            title="Screenshots"
            accept="image/*"
            helper="Upload project screenshots"
            onFiles={(files) =>
              setScreenshots([
                ...(screenshots || []),
                ...files.map((file) => ({
                  name: file.name.replace(/\.[^/.]+$/, ""),
                  file,
                })),
              ])
            }
          />
        ) : null}
        {showDiagrams ? (
          <DropzoneField
            title="Diagrams"
            accept="image/*"
            helper="Upload diagrams and set names"
            onFiles={(files) =>
              setDiagrams([
                ...(diagrams || []),
                ...files.map((file) => ({ name: file.name.replace(/\.[^/.]+$/, ""), file })),
              ])
            }
          />
        ) : null}
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        {showCode ? (
          <FileList title="Code Files" files={codeFiles || []} onRemove={(i) => setCodeFiles((codeFiles || []).filter((_, idx) => idx !== i))} />
        ) : null}
        {showScreenshots ? (
          <FileList
            title="Screenshots"
            files={screenshots || []}
            showNameInput
            onNameChange={(index, name) =>
              setScreenshots((screenshots || []).map((item, idx) => (idx === index ? { ...item, name } : item)))
            }
            onRemove={(i) => setScreenshots((screenshots || []).filter((_, idx) => idx !== i))}
          />
        ) : null}
        {showDiagrams ? (
          <FileList
            title="Diagrams"
            files={diagrams || []}
            showNameInput
            onNameChange={(index, name) =>
              setDiagrams((diagrams || []).map((item, idx) => (idx === index ? { ...item, name } : item)))
            }
            onRemove={(i) => setDiagrams((diagrams || []).filter((_, idx) => idx !== i))}
          />
        ) : null}
      </div>
    </div>
  );
}
