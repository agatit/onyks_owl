import { useParams } from "react-router-dom";
import Navbar from "../Components/Layout/Navbar";
import SideBar from "../Components/Layout/SideBar";
import ToolBar from "../Components/Layout/ToolBar";
import Diagrams from "../DiagramsM";

function EditorPage() {
  const { projectID }: { projectID: string } = useParams();

  return (
    <div>
      <Navbar />
      <div className="content">
        <SideBar projectId={projectID} />
        <Diagrams projectId={projectID} />
        <ToolBar projectId={projectID} />
      </div>
    </div>
  );
}

export default EditorPage;
