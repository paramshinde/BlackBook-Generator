import React from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import SplitPaneLayout from "../components/layout/SplitPaneLayout";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/project/local/project-details" replace />} />
        <Route path="/project/:projectId/:tab" element={<SplitPaneLayout />} />
      </Routes>
    </BrowserRouter>
  );
}
