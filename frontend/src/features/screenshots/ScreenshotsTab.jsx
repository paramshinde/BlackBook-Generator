import React from "react";
import ScreenshotUploader from "../../components/uploads/ScreenshotUploader";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function ScreenshotsTab() {
  const screenshots = useBlackbookStore((s) => s.screenshots);

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Screenshots</h2>
      <ScreenshotUploader />
      <div className="grid gap-3 sm:grid-cols-2">
        {screenshots.map((item, idx) => (
          <figure key={`${item.fileUrl || item.previewUrl}-${idx}`} className="rounded border bg-white p-2">
            <img src={item.previewUrl || item.fileUrl} alt={item.caption} className="mx-auto h-40 w-full object-contain" />
            <figcaption className="mt-2 text-center text-xs text-slate-700">
              Figure {idx + 1}: {item.caption || "Screenshot"}
            </figcaption>
          </figure>
        ))}
      </div>
    </div>
  );
}
