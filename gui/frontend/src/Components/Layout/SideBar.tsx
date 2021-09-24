import { useEffect, useState } from "react";
import ListModule from "../UI/ListModule";

import classes from "./SideBar.module.css";

function SideBar(props: any) {
  //const [isLoading, setIsLoading] = useState(true);
  const [loadedModules, setLoadedModules] = useState<any[]>([]);
  var counter = 0;

  async function loadModulesList() {
    const url = "modules-list.json";

    const resp = await fetch(url);
    const data = await resp.json();

    const modulesList: any[] = [];

    data.map((item: any) => {
      modulesList.push(item);
    });

    setLoadedModules(modulesList);
    return data;
  }

  useEffect(() => {
    loadModulesList();
  }, []);

  return (
    <div className={classes.sidebar}>
      <h2 className={classes.sidTitle}>Dostępne moduły:</h2>
      <ul>
        {loadedModules.map((module) => {
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
