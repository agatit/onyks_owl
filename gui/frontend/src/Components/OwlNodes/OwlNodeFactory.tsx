import * as React from "react";
import { OwlNodeModel } from "./OwlNodeModel";
import { OwlNodeWidget } from "./OwlNodeWidget";
import { AbstractReactFactory } from "@projectstorm/react-canvas-core";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";

export class OwlNodeFactory extends AbstractReactFactory<
  OwlNodeModel,
  DiagramEngine
> {
  constructor() {
    super("Owl-node");
  }

  generateModel(initialConfig: any) {
    return new OwlNodeModel(initialConfig);
  }

  generateReactWidget(event: { model: OwlNodeModel }): JSX.Element {
    return (
      <OwlNodeWidget engine={this.engine as DiagramEngine} node={event.model} />
    );
  }
}
