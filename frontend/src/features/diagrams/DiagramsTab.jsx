import React from "react";
import DiagramPanel from "../../components/diagrams/DiagramPanel";

export default function DiagramsTab() {
  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Diagrams</h2>
      <DiagramPanel />
    </div>
  );
}
