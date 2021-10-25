import {
  DefaultLinkFactory,
  DefaultLinkWidget,
  DiagramEngine,
} from "@projectstorm/react-diagrams";
import { OwlQueueLinkModel } from "./OwlQueueLinkModel";

export class OwlQueueLinkFactory extends DefaultLinkFactory {
  constructor() {
    super("OwlQueue");
  }

  generateModel() {
    return new OwlQueueLinkModel();
  }
}
