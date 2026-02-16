import React from "react";

const tabs = [
  { id: "details", label: "Details" },
  { id: "documentation", label: "Documentation" },
  { id: "code", label: "Code" },
  { id: "screenshots", label: "Screenshots" },
  { id: "diagrams", label: "Diagrams" },
  { id: "references", label: "References" },
  { id: "preview", label: "Preview" },
  { id: "export", label: "Export" },
];

export default function TabNavigation({ activeTab, onTabChange, completionByTab }) {
  return (
    <div className="sticky top-16 z-30 rounded-xl border border-slate-200 bg-white/95 p-2 shadow-sm backdrop-blur">
      <div className="grid grid-cols-2 gap-2 md:grid-cols-4 xl:grid-cols-8">
        {tabs.map((tab) => {
          const completion = completionByTab?.[tab.id] || 0;
          const active = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => onTabChange(tab.id)}
              className={`rounded-lg px-3 py-2 text-left text-xs transition ${
                active ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              <div className="font-semibold">{tab.label}</div>
              <div className={`mt-1 text-[10px] ${active ? "text-slate-200" : "text-slate-500"}`}>
                {completion}% complete
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
