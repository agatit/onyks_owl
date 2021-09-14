import { DiagramEngine } from "@projectstorm/react-diagrams";
import { NodeModel } from "../../CustomDiagramNodes/NodeModel";
import React from "react";

export interface BtnProps {
  engine: DiagramEngine;
}

export class AddNodeBtn extends React.Component<BtnProps> {
  engine: DiagramEngine;

  constructor(props: any) {
    super(props);
    this.engine = props.engine;
  }

  addDefaultNode = () => {
    this.engine.getModel().addAll(
      new NodeModel({
        color: "LemonChiffon",
        title: "Źródło OUT",
        content: "Source",
        source: true,
      })
    );
    this.engine.repaintCanvas();
  };

  render() {
    return (
      <button className=" add-button" onClick={this.addDefaultNode}>
        Dodaj moduł
      </button>
    );
  }
}

// TODO: Menu ustawiania parametrów dla generatora.
