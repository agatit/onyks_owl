import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { useRequest } from "redux-query-react";
import SideBar from "../Components/Layout/SideBar";
import ToolBar from "../Components/Layout/ToolBar";
import Diagrams from "../DiagramsM";
import { ProjectRequestConfig } from "../store/QueryConfigs";
import { getProject, Project } from "../store/redux-query";
import { selectProject } from "../store/selectors/projectSelectors";

function EditorPage() {
  const { projectID }: { projectID: string } = useParams();

  const [{ isPending, status }, refresh] = useRequest(
    getProject({ projectId: projectID }, ProjectRequestConfig)
  );

  const project: Project = useSelector(selectProject);

  return (
    <div className="content">
      <SideBar projectId={projectID} />
      <Diagrams projectInfo={project} projectId={projectID} />
      <ToolBar projectId={projectID} />
    </div>
  );
}

export default EditorPage;
