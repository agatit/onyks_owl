import React from "react";
import data from "../../data/testSchema.json";
import classses from "./Toolbar.module.css";
import Button from "../UI/Button";
import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams-core";

interface toolBarProps {
  engine: DiagramEngine;
}

function ToolBar(props: toolBarProps) {
  const engine = props.engine;

  function loadSchema() {
    var newModel = new DiagramModel();
    var modelString = JSON.stringify(data);
    newModel.deserializeModel(JSON.parse(modelString), engine);

    engine.setModel(newModel);
  }

  return (
    <div className={classses.toolBar}>
      <h2>Narzędzia:</h2>
      <Button
        text="Zapisz schemat"
        action={() => console.log(props.engine.getModel().serialize())}
      />
      <Button text="Wczytaj schemat" action={loadSchema} />
    </div>
  );
}

export default ToolBar;
