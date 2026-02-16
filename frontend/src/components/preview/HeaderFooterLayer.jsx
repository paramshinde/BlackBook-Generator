import React from "react";

export default function HeaderFooterLayer({ meta, pageNo }) {
  return (
    <>
      <div className="preview-header">{meta.projectTitle || "BLACK BOOK GENERATOR"}</div>
      <div className="preview-footer">
        <span>{meta.studentName || "Student"}</span>
        <span>Page {pageNo}</span>
      </div>
    </>
  );
}
