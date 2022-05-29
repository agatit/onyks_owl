import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { useRequest } from "redux-query-react";
import Navbar from "../Components/Layout/Navbar";
import PlayerMenu from "../Components/UI/Menu-UI/PlayerMenu";
import Diagrams from "../DiagramsM";
import { ProjectRequestConfig } from "../store/QueryConfigs";
import { getProject, Project } from "../store/redux-query";
import { selectProject } from "../store/selectors/projectSelectors";

function PlayerPage() {
  const { projectID }: { projectID: string } = useParams();

  const [{ isPending, status }, refresh] = useRequest(
    getProject({ projectId: projectID }, ProjectRequestConfig)
  );

  const project: Project = useSelector(selectProject);

  return (
    <div>
      <Navbar />
      <PlayerMenu />
      <div className="content player-content">
        <Diagrams projectId={projectID} />
      </div>
    </div>
  );
}

export default PlayerPage;
