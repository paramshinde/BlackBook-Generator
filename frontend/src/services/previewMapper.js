const esc = (s = "") =>
  s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br />");

export function mapDocumentToPreviewHtml(document) {
  const toc = document.toc
    .map((entry) => `<div class="toc-entry"><span>${esc(entry.title)}</span><span>${entry.page}</span></div>`)
    .join("");

  const sections = document.sections
    .map(
      (section) =>
        `<section><h2>${esc(section.heading)}</h2><p>${esc(section.content)}</p></section>`
    )
    .join("");

  const figures = document.figures
    .map(
      (f, i) =>
        `<figure><img src="${f.previewUrl || f.fileUrl || ""}" alt="${esc(f.caption || "Screenshot")}" style="max-width:100%" /><figcaption>Figure ${i + 1}: ${esc(
          f.caption || "Screenshot"
        )}</figcaption></figure>`
    )
    .join("");

  return `<article><h1>${esc(document.meta.projectTitle || "Untitled Project")}</h1><h3>Table of Contents</h3>${toc}${sections}${figures}</article>`;
}
