import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../../services/apiClient";

export default function ExportPanel() {
  const { projectId = "local" } = useParams();
  const [status, setStatus] = useState("");

  const createExport = async (type) => {
    setStatus(`Creating ${type.toUpperCase()} export...`);
    const route = type === "docx" ? apiClient.exportDocx : type === "pdf" ? apiClient.exportPdf : apiClient.exportZip;
    try {
      const { data } = await route(projectId);
      setStatus(`Job queued: ${data.job_id}`);
    } catch (error) {
      setStatus("Export request failed");
    }
  };

  return (
    <div className="space-y-3 rounded border border-slate-200 bg-white p-4">
      <div className="flex gap-2">
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => createExport("docx")}>DOCX</button>
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => createExport("pdf")}>PDF</button>
        <button className="rounded bg-slate-900 px-3 py-2 text-white" onClick={() => createExport("zip")}>ZIP</button>
      </div>
      <p className="text-sm text-slate-600">{status}</p>
    </div>
  );
}
