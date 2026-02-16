import React from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../../services/apiClient";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function ScreenshotUploader() {
  const { projectId = "local" } = useParams();
  const addScreenshot = useBlackbookStore((s) => s.addScreenshot);

  const onUpload = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const { data } = await apiClient.uploadScreenshots(projectId, formData);
      (data.items || []).forEach((item) => addScreenshot(item));
    } catch (error) {
      console.error(error);
      files.forEach((file, idx) => {
        addScreenshot({
          fileUrl: "",
          previewUrl: URL.createObjectURL(file),
          caption: file.name,
          figureNo: `Figure ${idx + 1}`,
        });
      });
    }
  };

  return <input type="file" multiple accept="image/*" onChange={onUpload} className="w-full rounded border p-2" />;
}
