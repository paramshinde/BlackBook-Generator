import React from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../../services/apiClient";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function CodeUploader() {
  const { projectId = "local" } = useParams();
  const upsertCodeFile = useBlackbookStore((s) => s.upsertCodeFile);

  const onUpload = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    try {
      const { data } = await apiClient.uploadCode(projectId, formData);
      (data.items || []).forEach((item) => upsertCodeFile(item));
    } catch (error) {
      console.error(error);
      files.forEach(async (file) => {
        const content = await file.text();
        upsertCodeFile({ filename: file.name, language: "text", content_text: content });
      });
    }
  };

  return <input type="file" multiple onChange={onUpload} className="w-full rounded border p-2" />;
}
