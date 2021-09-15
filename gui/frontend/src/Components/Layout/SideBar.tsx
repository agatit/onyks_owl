import { useState } from "react";
import ListModule from "../UI/ListModule";

import classes from "./SideBar.module.css";

const DUMMY_DATA = [
  {
    name: "Moduł wykrywający ruch",
  },
  {
    name: "Moduł testowy",
  },
];

function SideBar(props: any) {
  // REDUX ?? ..
  const [isLoading, setIsLoading] = useState(true);
  const [loadedModules, setLoadedModules] = useState([]);
  var counter = 0;

  return (
    <div className={classes.sidebar}>
      <h2 className={classes.sidTitle}>Dostępne moduły:</h2>
      <ul>
        {DUMMY_DATA.map((module) => {
          counter++;
          return (
            <li key={counter}>
              <ListModule module={module} />
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default SideBar;
