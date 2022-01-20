import ModuleList from "../UI/Menu-UI/ModuleList";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import classes from "./SideBar.module.css";
import { faCubes } from "@fortawesome/free-solid-svg-icons";

function SideBar(props: any) {
  return (
    <div className={classes.sidebar}>
      <div className={classes.sidTitle}>
        <FontAwesomeIcon icon={faCubes} size="3x" />
      </div>
      <ModuleList projectId={props.projectId} />
    </div>
  );
}

export default SideBar;
