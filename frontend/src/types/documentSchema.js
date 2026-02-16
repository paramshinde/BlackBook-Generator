export const sectionKeys = [
  "introduction",
  "objective",
  "scope",
  "techStack",
  "modules",
  "conclusion",
];

export const defaultDocument = {
  meta: {
    projectTitle: "",
    studentName: "",
    guideName: "",
    professorName: "",
    techStack: "",
    year: "",
  },
  sections: sectionKeys.map((key, idx) => ({
    id: key,
    heading: `${idx + 1}. ${key.replace(/([A-Z])/g, " $1").replace(/^./, (c) => c.toUpperCase())}`,
    content: "",
    order: idx + 1,
  })),
  diagrams: [],
  codeBlocks: [],
  figures: [],
  toc: [],
  templateSettings: {
    template: "ieee",
    darkPreview: false,
    margins: { top: 64, right: 70, bottom: 64, left: 70 },
    fontFamily: "Source Serif 4",
    fontSize: 12,
  },
};
