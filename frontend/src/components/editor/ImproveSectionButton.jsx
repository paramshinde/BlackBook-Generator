import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { apiClient } from "../../services/apiClient";
import { useBlackbookStore } from "../../store/useBlackbookStore";

export default function ImproveSectionButton({ sectionKey, currentContent }) {
  const { projectId = "local" } = useParams();
  const setSectionContent = useBlackbookStore((s) => s.setSectionContent);
  const [loading, setLoading] = useState(false);

  const onImprove = async () => {
    if (!currentContent.trim()) return;
    setLoading(true);
    try {
      const { data } = await apiClient.improveSection(projectId, sectionKey, {
        content: currentContent,
        target_words: 220,
      });
      setSectionContent(sectionKey, data.improved_text || currentContent);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={onImprove}
      disabled={loading}
      className="rounded bg-amber-500 px-3 py-2 text-xs font-semibold text-white hover:bg-amber-600 disabled:opacity-60"
    >
      {loading ? "Improving..." : "? Improve this Section"}
    </button>
  );
}
