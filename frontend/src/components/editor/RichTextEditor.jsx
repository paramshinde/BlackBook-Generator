import React, { useEffect } from "react";
import StarterKit from "@tiptap/starter-kit";
import { EditorContent, useEditor } from "@tiptap/react";

export default function RichTextEditor({ value, onChange }) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: value,
    onUpdate: ({ editor: instance }) => {
      onChange(instance.getText());
    },
    editorProps: {
      attributes: {
        class:
          "min-h-[220px] rounded border border-slate-300 bg-white p-3 text-sm leading-6 focus:outline-none",
      },
      handlePaste(view, event) {
        const text = event.clipboardData?.getData("text/plain") || "";
        if (!text.trim()) return false;
        const normalized = text
          .split("\n")
          .map((line) => (line.trim().startsWith("-") ? `• ${line.replace(/^-+\s*/, "")}` : line))
          .join("\n");
        view.dispatch(view.state.tr.insertText(normalized));
        return true;
      },
    },
  });

  useEffect(() => {
    if (editor && editor.getText() !== value) {
      editor.commands.setContent(value || "");
    }
  }, [value, editor]);

  return <EditorContent editor={editor} />;
}
