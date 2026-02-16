import React from "react";
import HeaderFooterLayer from "./HeaderFooterLayer";

export default function A4Page({ children, dark, meta, pageNo }) {
  return (
    <article className={`preview-page ${dark ? "dark" : ""}`}>
      <HeaderFooterLayer meta={meta} pageNo={pageNo} />
      {children}
    </article>
  );
}
