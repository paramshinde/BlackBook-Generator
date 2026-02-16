import React from "react";

export default function TocPreview({ toc }) {
  return (
    <section className="mb-8">
      <h2 className="font-serif text-xl font-semibold">Table of Contents</h2>
      <div className="mt-3 space-y-1 text-sm">
        {toc.map((entry, idx) => (
          <div key={`${entry.title}-${idx}`} className="toc-entry">
            <span>{entry.title}</span>
            <span>{entry.page}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
