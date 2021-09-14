import React from "react";

import classses from "./Toolbar.module.css";
import { AddNodeBtn } from "../UI/Menu-UI/Buttons/NodeGenerator";

function ToolBar(props: any) {
  return (
    <div className={classses.toolBar}>
      <h2>Narzędzia:</h2>
      <AddNodeBtn engine={props.engine} />
      <button type="submit" className="add-button">
        test
      </button>
    </div>
  );
}

export default ToolBar;
