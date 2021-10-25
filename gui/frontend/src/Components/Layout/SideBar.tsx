import ModuleList from "../UI/Menu-UI/ModuleList";

import classes from "./SideBar.module.css";

function SideBar(props: any) {
  return (
    <div className={classes.sidebar}>
      <h2 className={classes.sidTitle}>Dostępne moduły:</h2>
      <ModuleList projectId={props.projectId} />
    </div>
  );
}

export default SideBar;
