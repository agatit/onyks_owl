import React from "react";
import data from "../../data/testSchema3.json";
import classses from "./Toolbar.module.css";
import Button from "../UI/Button";
import { DiagramEngine, DiagramModel } from "@projectstorm/react-diagrams-core";
import getNotification, { NotificationType } from "../UI/Notification";
import { NodeModel } from "../CustomDiagramNodes/NodeModel";
import { connect } from "react-redux";
import { store } from "../../store/store";

interface toolBarProps {
  engine: DiagramEngine;
  node?: NodeModel;
  test?: string;
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
        action={() => {
          console.log(props.engine.getModel().serialize());
          getNotification({
            text: "Pomyślnie zapisano schemat!",
            type: NotificationType.SUCCESS,
            position: "bottom-left",
          });
        }}
      />
      <Button text="Wczytaj schemat" action={loadSchema} />
      <h1>{props.test}</h1>
    </div>
  );
}

export default ToolBar;

const mapStateToProps = (state: any) => {
  return { node: state.selectedNode, test: state.test };
};

connect(mapStateToProps)(ToolBar);
