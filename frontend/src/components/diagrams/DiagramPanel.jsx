import React, { useState } from "react";
import { useParams } from "react-router-dom";
import MermaidRenderer from "./MermaidRenderer";
import { apiClient } from "../../services/apiClient";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function DiagramPanel() {
  const { projectId = "local" } = useParams();
  const projectTitle = useBlackbookStore((s) => s.projectDetails.projectTitle);
  const diagrams = useBlackbookStore((s) => s.diagramData);
  const setDiagrams = useBlackbookStore((s) => s.setDiagrams);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    try {
      const { data } = await apiClient.generateDiagrams(projectId, { project_title: projectTitle });
      setDiagrams(data.diagrams || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <button onClick={generate} className="rounded bg-blue-600 px-4 py-2 text-white" disabled={loading}>
        {loading ? "Generating..." : "Generate Diagrams"}
      </button>
      {diagrams.map((diagram) => (
        <div key={diagram.diagram_type} className="space-y-1">
          <h4 className="text-sm font-semibold">{diagram.diagram_type}</h4>
          <MermaidRenderer code={diagram.mermaid_code} />
        </div>
      ))}
    </div>
  );
}
