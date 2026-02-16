import { create } from "zustand";
import { persist } from "zustand/middleware";
import { defaultDocument } from "../types/documentSchema";

const templateMap = {
  ieee: {
    fontFamily: "Source Serif 4",
    fontSize: 11,
    margins: { top: 64, right: 70, bottom: 64, left: 70 },
  },
  college: {
    fontFamily: "Times New Roman",
    fontSize: 12,
    margins: { top: 72, right: 72, bottom: 72, left: 72 },
  },
};

export const useBlackbookStore = create(
  persist(
    (set, get) => ({
      projectDetails: defaultDocument.meta,
      documentationSections: defaultDocument.sections,
      diagramData: [],
      codeFiles: [],
      screenshots: [],
      templateSettings: defaultDocument.templateSettings,
      versionHistory: [],
      activeTab: "project-details",
      isSaving: false,
      setActiveTab: (activeTab) => set({ activeTab }),
      setProjectDetail: (key, value) =>
        set((state) => ({ projectDetails: { ...state.projectDetails, [key]: value } })),
      setSectionContent: (id, content) =>
        set((state) => ({
          documentationSections: state.documentationSections.map((section) =>
            section.id === id ? { ...section, content } : section
          ),
        })),
      setTemplate: (template) =>
        set((state) => ({
          templateSettings: {
            ...state.templateSettings,
            template,
            ...(templateMap[template] || {}),
          },
        })),
      setDarkPreview: (darkPreview) =>
        set((state) => ({ templateSettings: { ...state.templateSettings, darkPreview } })),
      addDiagram: (diagram) => set((state) => ({ diagramData: [...state.diagramData, diagram] })),
      setDiagrams: (diagramData) => set({ diagramData }),
      upsertCodeFile: (file) =>
        set((state) => {
          const exists = state.codeFiles.some((f) => f.filename === file.filename);
          return {
            codeFiles: exists
              ? state.codeFiles.map((f) => (f.filename === file.filename ? file : f))
              : [...state.codeFiles, file],
          };
        }),
      addScreenshot: (screenshot) =>
        set((state) => ({ screenshots: [...state.screenshots, screenshot] })),
      saveSnapshot: (note = "Autosave") =>
        set((state) => ({
          versionHistory: [
            {
              id: crypto.randomUUID(),
              createdAt: new Date().toISOString(),
              note,
              snapshot: {
                projectDetails: state.projectDetails,
                documentationSections: state.documentationSections,
                diagramData: state.diagramData,
                codeFiles: state.codeFiles,
                screenshots: state.screenshots,
                templateSettings: state.templateSettings,
              },
            },
            ...state.versionHistory,
          ].slice(0, 20),
        })),
      restoreVersion: (versionId) => {
        const version = get().versionHistory.find((v) => v.id === versionId);
        if (!version) return;
        set({ ...version.snapshot });
      },
      toDocumentJson: () => {
        const state = get();
        const toc = state.documentationSections
          .filter((s) => s.content.trim())
          .map((s, index) => ({ level: 1, title: s.heading, page: index + 2 }));

        return {
          meta: state.projectDetails,
          sections: state.documentationSections,
          diagrams: state.diagramData,
          codeBlocks: state.codeFiles,
          figures: state.screenshots,
          toc,
          templateSettings: state.templateSettings,
        };
      },
    }),
    { name: "blackbook-store-v1" }
  )
);
