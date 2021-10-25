import * as React from "react";
import { NodeModel } from "./NodeModel";
import { NodeWidget } from "./NodeWidget";
import { AbstractReactFactory } from "@projectstorm/react-canvas-core";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";

export class NodeFactory extends AbstractReactFactory<
  NodeModel,
  DiagramEngine
> {
  constructor() {
    super("ts-custom-node");
  }

  generateModel(initialConfig: any) {
    return new NodeModel(initialConfig);
  }

  generateReactWidget(event: { model: NodeModel }): JSX.Element {
    return (
      <NodeWidget engine={this.engine as DiagramEngine} node={event.model} />
    );
  }
}
