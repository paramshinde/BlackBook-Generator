import React from "react";

export default function LoadingOverlay({ show, label = "Processing..." }) {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-[90] flex items-center justify-center bg-slate-950/45">
      <div className="rounded-xl bg-white px-6 py-5 shadow-2xl">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-300 border-t-slate-900" />
          <span className="text-sm font-semibold text-slate-700">{label}</span>
        </div>
      </div>
    </div>
  );
}
