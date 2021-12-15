import { OwlQueueModel } from "./OwlQueueModel";
import { AbstractReactFactory } from "@projectstorm/react-canvas-core";
import { DiagramEngine } from "@projectstorm/react-diagrams-core";
import { DefaultNodeWidget } from "@projectstorm/react-diagrams-defaults";

export class OwlQueueFactory extends AbstractReactFactory<
  OwlQueueModel,
  DiagramEngine
> {
  constructor() {
    super("OwlQueue");
  }

  generateReactWidget(event: { model: OwlQueueModel }): JSX.Element {
    return <DefaultNodeWidget node={event.model} engine={this.engine} />;
  }

  generateModel(event: any) {
    return new OwlQueueModel();
  }
}
