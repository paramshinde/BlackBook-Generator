import React from "react";

export default function ProgressHeader({ completion }) {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Black Book Generator</h1>
          <p className="text-xs text-slate-500">AI-Powered Project Documentation Dashboard</p>
        </div>
        <div className="w-56">
          <div className="mb-1 flex items-center justify-between text-xs text-slate-600">
            <span>Completion</span>
            <span>{completion}%</span>
          </div>
          <div className="h-2 rounded-full bg-slate-200">
            <div className="h-2 rounded-full bg-emerald-500 transition-all" style={{ width: `${completion}%` }} />
          </div>
        </div>
      </div>
    </header>
  );
}
