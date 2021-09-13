import createEngine from "@projectstorm/react-diagrams";
import * as React from "react";
import { Menu } from "./Menu-UI/Menu";
import { Diagrams } from "./DiagramsM";
import "./styles.css";

const engine = createEngine();

export default function App() {
  return (
    <div>
      <div className="App">
        <Diagrams engine={engine} />
      </div>
      <div className="sidenav">
        <Menu engine={engine} />
      </div>
    </div>
  );
}
