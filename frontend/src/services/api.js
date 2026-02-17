import axios from "axios";
import { toApiUrl } from "./apiBase";

const api = axios.create({ baseURL: toApiUrl("/api") });

function parseAxiosError(error, fallback = "Request failed") {
  const payload = error?.response?.data || {};
  const message =
    payload?.data?.error ||
    payload?.message ||
    error?.message ||
    fallback;
  return new Error(message);
}

function unwrapResponse(response) {
  const payload = response?.data || {};
  if (!payload.success) {
    throw new Error(payload.message || "Request failed");
  }
  return payload.data;
}

export async function fetchTemplates() {
  try {
    const response = await api.get("/templates");
    return unwrapResponse(response).templates || [];
  } catch (error) {
    throw parseAxiosError(error, "Failed to fetch templates");
  }
}

export async function requestPreview(payload) {
  try {
    const response = await api.post("/preview", payload);
    return unwrapResponse(response);
  } catch (error) {
    throw parseAxiosError(error, "Failed to render preview");
  }
}

export async function requestAIContent(projectTitle) {
  try {
    const response = await api.post("/generate-ai", { project_title: projectTitle });
    return unwrapResponse(response).documentation || {};
  } catch (error) {
    throw parseAxiosError(error, "AI generation failed");
  }
}

export async function uploadFiles(formData) {
  try {
    const response = await api.post("/upload-files", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return unwrapResponse(response);
  } catch (error) {
    throw parseAxiosError(error, "File upload failed");
  }
}

export async function generateDocument(formData) {
  try {
    const response = await api.post("/generate-document", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return unwrapResponse(response);
  } catch (error) {
    throw parseAxiosError(error, "Document generation failed");
  }
}

export async function downloadFile(downloadUrl, fileName = "blackbook.docx") {
  try {
    const normalized = downloadUrl?.startsWith("/api/") ? downloadUrl.replace(/^\/api/, "") : downloadUrl;
    const response = await api.get(normalized, { responseType: "blob" });
    const blobUrl = window.URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = blobUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(blobUrl);
  } catch (error) {
    throw parseAxiosError(error, "Download failed");
  }
}
