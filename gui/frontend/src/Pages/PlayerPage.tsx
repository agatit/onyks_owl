import Navbar from "../Components/Layout/Navbar";
import PlayerMenu from "../Components/UI/Menu-UI/PlayerMenu";
import classes from "./PlayerPage.module.css";
import Diagrams from "../DiagramsM";

function PlayerPage() {
  return (
    <div>
      <Navbar />
      <PlayerMenu />
      <div className="content player-content">
        <Diagrams />
      </div>
    </div>
  );
}

export default PlayerPage;
