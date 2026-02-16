import React, { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({ startOnLoad: false, theme: "neutral" });

export default function MermaidRenderer({ code }) {
  const ref = useRef(null);

  useEffect(() => {
    let active = true;
    async function render() {
      if (!ref.current || !code) return;
      try {
        const id = `m-${Math.random().toString(36).slice(2)}`;
        const { svg } = await mermaid.render(id, code);
        if (active) ref.current.innerHTML = svg;
      } catch (e) {
        if (active) ref.current.innerHTML = `<pre>${e.message}</pre>`;
      }
    }
    render();
    return () => {
      active = false;
    };
  }, [code]);

  return <div ref={ref} className="rounded border border-slate-200 bg-white p-3" />;
}
