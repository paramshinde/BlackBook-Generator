import React from "react";
import { useParams } from "react-router-dom";
import ProjectDetailsTab from "../../features/project-details/ProjectDetailsTab";
import DocumentationTab from "../../features/documentation/DocumentationTab";
import DiagramsTab from "../../features/diagrams/DiagramsTab";
import CodeTab from "../../features/code/CodeTab";
import ScreenshotsTab from "../../features/screenshots/ScreenshotsTab";
import FinalExportTab from "../../features/final-export/FinalExportTab";

const map = {
  "project-details": ProjectDetailsTab,
  documentation: DocumentationTab,
  diagrams: DiagramsTab,
  code: CodeTab,
  screenshots: ScreenshotsTab,
  "final-export": FinalExportTab,
};

export default function LeftFormPane() {
  const { tab = "project-details" } = useParams();
  const Component = map[tab] || ProjectDetailsTab;

  return (
    <div className="h-[calc(100vh-62px)] overflow-y-auto bg-slate-50 p-4">
      <Component />
    </div>
  );
}
