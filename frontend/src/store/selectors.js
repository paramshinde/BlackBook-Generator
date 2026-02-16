export const selectCompletion = (state) => {
  const requiredMeta = ["projectTitle", "studentName", "guideName"];
  const metaScore = requiredMeta.reduce(
    (acc, key) => acc + (state.projectDetails[key]?.trim() ? 1 : 0),
    0
  );
  const sectionScore = state.documentationSections.reduce(
    (acc, section) => acc + (section.content.trim() ? 1 : 0),
    0
  );
  const total = requiredMeta.length + state.documentationSections.length;
  return Math.round(((metaScore + sectionScore) / total) * 100);
};
