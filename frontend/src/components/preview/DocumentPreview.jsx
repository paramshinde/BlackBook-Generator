import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { useBlackbookStore } from "../../store/useBlackbookStore";
import { debounce } from "../../services/debounce";
import { apiClient } from "../../services/apiClient";
import { mapDocumentToPreviewHtml } from "../../services/previewMapper";
import A4Page from "./A4Page";
import TocPreview from "./TocPreview";

export default function DocumentPreview() {
  const { projectId = "local" } = useParams();
  const toDocumentJson = useBlackbookStore((s) => s.toDocumentJson);
  const saveSnapshot = useBlackbookStore((s) => s.saveSnapshot);
  const documentJson = toDocumentJson();
  const [html, setHtml] = useState(mapDocumentToPreviewHtml(documentJson));

  const syncPreview = useMemo(
    () =>
      debounce(async (payload) => {
        try {
          const { data } = await apiClient.renderPreview(projectId, {
            document: payload,
            templateSettings: payload.templateSettings,
          });
          setHtml(data.html || mapDocumentToPreviewHtml(payload));
        } catch (error) {
          setHtml(mapDocumentToPreviewHtml(payload));
        }
      }, 300),
    [projectId]
  );

  const syncSave = useMemo(
    () =>
      debounce(async (payload) => {
        try {
          await apiClient.autosave(projectId, { document: payload });
          saveSnapshot("Autosave");
        } catch (error) {
          console.error(error);
        }
      }, 1000),
    [projectId, saveSnapshot]
  );

  useEffect(() => {
    syncPreview(documentJson);
    syncSave(documentJson);
  }, [documentJson, syncPreview, syncSave]);

  return (
    <div>
      <A4Page dark={documentJson.templateSettings.darkPreview} meta={documentJson.meta} pageNo={1}>
        <TocPreview toc={documentJson.toc} />
        <div className="prose max-w-none font-serif" dangerouslySetInnerHTML={{ __html: html }} />
      </A4Page>
    </div>
  );
}
