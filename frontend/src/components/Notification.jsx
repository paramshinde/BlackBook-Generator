import React from "react";

const toneMap = {
  success: "border-emerald-200 bg-emerald-50 text-emerald-700",
  error: "border-red-200 bg-red-50 text-red-700",
  info: "border-blue-200 bg-blue-50 text-blue-700",
};

export default function Notification({ toasts, onDismiss }) {
  if (!toasts?.length) return null;

  return (
    <div className="fixed right-4 top-20 z-[70] space-y-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`flex min-w-72 items-start justify-between gap-4 rounded-xl border px-4 py-3 text-sm shadow-lg ${
            toneMap[toast.type] || toneMap.info
          }`}
        >
          <span>{toast.message}</span>
          <button
            type="button"
            className="text-xs font-semibold opacity-70 hover:opacity-100"
            onClick={() => onDismiss(toast.id)}
          >
            Close
          </button>
        </div>
      ))}
    </div>
  );
}
