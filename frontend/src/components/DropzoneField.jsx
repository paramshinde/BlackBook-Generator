import React, { useRef, useState } from "react";

export default function DropzoneField({ title, accept, onFiles, helper }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    const files = Array.from(event.dataTransfer.files || []);
    if (files.length) onFiles(files);
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`rounded-xl border-2 border-dashed p-4 transition ${
        dragging ? "border-slate-900 bg-slate-100" : "border-slate-300 bg-white"
      }`}
    >
      <p className="text-sm font-semibold text-slate-800">{title}</p>
      <p className="mt-1 text-xs text-slate-500">{helper}</p>
      <div className="mt-3 flex items-center gap-2">
        <button
          type="button"
          className="rounded-lg bg-slate-900 px-3 py-2 text-xs font-semibold text-white"
          onClick={() => inputRef.current?.click()}
        >
          Choose Files
        </button>
        <span className="text-xs text-slate-500">or drag and drop</span>
      </div>
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={accept}
        className="hidden"
        onChange={(e) => onFiles(Array.from(e.target.files || []))}
      />
    </div>
  );
}
