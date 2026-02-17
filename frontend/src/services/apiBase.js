const rawBaseUrl = (import.meta.env.VITE_API_BASE_URL || "").trim();

function stripTrailingSlash(value) {
  return value.replace(/\/+$/, "");
}

export const API_BASE_URL = rawBaseUrl ? stripTrailingSlash(rawBaseUrl) : "";

export function toApiUrl(path) {
  if (!path) return API_BASE_URL || "/";
  if (/^https?:\/\//i.test(path)) return path;
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${normalized}`;
}

