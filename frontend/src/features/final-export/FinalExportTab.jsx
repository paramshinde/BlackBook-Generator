import React, { useState } from "react";
import ExportPanel from "../../components/export/ExportPanel";
import { useParams } from "react-router-dom";
import { apiClient } from "../../services/apiClient";
import { useBlackbookStore } from "../../store/useBlackbookStore";
import { selectCompletion } from "../../store/selectors";

export default function FinalExportTab() {
  const { projectId = "local" } = useParams();
  const store = useBlackbookStore();
  const completion = selectCompletion(store);
  const [plagiarism, setPlagiarism] = useState(null);

  const checkPlagiarism = async () => {
    try {
      const { data } = await apiClient.plagiarismCheck(projectId, { document: store.toDocumentJson() });
      setPlagiarism(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Final Export</h2>
      <div className="rounded bg-white p-4">
        <div className="mb-2 flex items-center justify-between text-sm font-semibold">
          <span>Completion</span>
          <span>{completion}%</span>
        </div>
        <div className="h-2 rounded bg-slate-200">
          <div className="h-2 rounded bg-emerald-500" style={{ width: `${completion}%` }} />
        </div>
      </div>
      <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={checkPlagiarism}>
        Run Plagiarism Check
      </button>
      {plagiarism && (
        <div className="rounded border bg-white p-3 text-sm">
          <div>Originality: {plagiarism.originality_percentage}%</div>
          <div>Suspicious sections: {plagiarism.flagged_sections?.length || 0}</div>
        </div>
      )}
      <ExportPanel />
    </div>
  );
}
