import React from "react";
import SectionEditor from "../../components/editor/SectionEditor";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function DocumentationTab() {
  const sections = useBlackbookStore((s) => s.documentationSections);
  const setSectionContent = useBlackbookStore((s) => s.setSectionContent);

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-slate-900">Documentation</h2>
      {sections.map((section) => (
        <SectionEditor
          key={section.id}
          section={section}
          onChange={(content) => setSectionContent(section.id, content)}
        />
      ))}
    </div>
  );
}
