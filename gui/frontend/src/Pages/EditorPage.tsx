import Navbar from "../Components/Layout/Navbar";
import SideBar from "../Components/Layout/SideBar";
import ToolBar from "../Components/Layout/ToolBar";
import Diagrams from "../DiagramsM";

function EditorPage() {
  return (
    <div>
      <Navbar />
      <div className="content">
        <SideBar />
        <Diagrams />
        <ToolBar />
      </div>
    </div>
  );
}

export default EditorPage;
