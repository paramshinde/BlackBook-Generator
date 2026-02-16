import React from "react";
import RichTextEditor from "./RichTextEditor";
import ImproveSectionButton from "./ImproveSectionButton";

export default function SectionEditor({ section, onChange }) {
  return (
    <div className="space-y-2 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-slate-800">{section.heading}</h3>
        <ImproveSectionButton sectionKey={section.id} currentContent={section.content} />
      </div>
      <RichTextEditor value={section.content} onChange={onChange} />
    </div>
  );
}
