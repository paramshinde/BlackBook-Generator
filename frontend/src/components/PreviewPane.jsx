import React from "react";

export default function PreviewPane({ html, loading }) {
  return (
    <div className="min-h-[65vh] rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {loading ? (
        <div className="flex items-center gap-3 text-sm text-slate-500">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-slate-800" />
          Updating preview...
        </div>
      ) : (
        <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: html }} />
      )}
    </div>
  );
}
