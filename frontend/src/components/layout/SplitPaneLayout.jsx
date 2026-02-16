import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TopNavTabs from "./TopNavTabs";
import LeftFormPane from "./LeftFormPane";
import RightPreviewPane from "./RightPreviewPane";
import { apiClient } from "../../services/apiClient";

export default function SplitPaneLayout() {
  const { projectId, tab = "project-details" } = useParams();
  const navigate = useNavigate();
  const [bootstrapping, setBootstrapping] = useState(projectId === "local");

  useEffect(() => {
    async function bootstrapProject() {
      if (projectId !== "local") return;
      try {
        const { data } = await apiClient.createProject({
          title: "Untitled Black Book",
          guide_name: "",
          template: "ieee",
        });
        navigate(`/project/${data.id}/${tab}`, { replace: true });
      } catch (error) {
        console.error(error);
      } finally {
        setBootstrapping(false);
      }
    }

    bootstrapProject();
  }, [projectId, tab, navigate]);

  if (bootstrapping) {
    return <div className="flex min-h-screen items-center justify-center text-slate-600">Initializing project...</div>;
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <TopNavTabs />
      <div className="grid grid-cols-1 lg:grid-cols-2">
        <LeftFormPane />
        <RightPreviewPane />
      </div>
    </div>
  );
}
