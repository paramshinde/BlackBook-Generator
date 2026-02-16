import React from "react";
import { Link, useParams } from "react-router-dom";
import { useBlackbookStore } from "../../store/useBlackbookStore";

const tabs = [
  { key: "project-details", label: "Project Details" },
  { key: "documentation", label: "Documentation" },
  { key: "diagrams", label: "Diagrams" },
  { key: "code", label: "Code Implementation" },
  { key: "screenshots", label: "Screenshots" },
  { key: "final-export", label: "Final Export" },
];

export default function TopNavTabs() {
  const { projectId, tab } = useParams();
  const setActiveTab = useBlackbookStore((s) => s.setActiveTab);

  return (
    <nav className="flex flex-wrap gap-2 border-b border-slate-200 p-3 bg-white">
      {tabs.map((item) => (
        <Link
          key={item.key}
          to={`/project/${projectId || "local"}/${item.key}`}
          onClick={() => setActiveTab(item.key)}
          className={`rounded px-3 py-2 text-sm font-semibold transition ${
            tab === item.key ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
