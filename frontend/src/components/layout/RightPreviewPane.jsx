import React from "react";
import DocumentPreview from "../preview/DocumentPreview";

export default function RightPreviewPane() {
  return (
    <div className="h-[calc(100vh-62px)] overflow-y-auto bg-slate-200 p-4">
      <DocumentPreview />
    </div>
  );
}
